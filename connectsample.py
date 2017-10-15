import json
import sys
import uuid
import time
import requests
from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauthlib.client import OAuth
import news_scraper
from scoreImage import scoreImage, parseScore
from pygameImage import takePic

# read private credentials from text file
client_id, client_secret, *_ = open('_PRIVATE.txt').read().split('\n')
if (client_id.startswith('*') and client_id.endswith('*')) or \
    (client_secret.startswith('*') and client_secret.endswith('*')):
    print('MISSING CONFIGURATION: the _PRIVATE.txt file needs to be edited ' + \
        'to add client ID and secret.')
    sys.exit(1)

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

# since this sample runs locally without HTTPS, disable InsecureRequestWarning
requests.packages.urllib3.disable_warnings()

msgraphapi = oauth.remote_app( \
    'microsoft',
    consumer_key=client_id,
    consumer_secret=client_secret,
    request_token_params={'scope': 'User.Read Mail.Send People.Read'},
    base_url='https://graph.microsoft.com/v1.0/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
    authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
                             )

# shit for the news reader

news_site = 'http://cnn.com'
news = news_scraper.buildArticleBase(news_site)

@app.route('/')
def index():
    """Handler for home page."""
    return render_template('connect.html')

@app.route('/login')
def login():
    """Handler for login route."""
    guid = uuid.uuid4() # guid used to only accept initiated logins
    session['state'] = guid
    return msgraphapi.authorize(callback=url_for('authorized', _external=True), state=guid)

@app.route('/logout')
def logout():
    """Handler for logout route."""
    session.pop('microsoft_token', None)
    session.pop('state', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    """Handler for login/authorized route."""
    response = msgraphapi.authorized_response()

    if response is None:
        return "Access Denied: Reason={0}\nError={1}".format( \
            request.args['error'], request.args['error_description'])

    # Check response for state
    if str(session['state']) != str(request.args['state']):
        raise Exception('State has been messed with, end authentication')
    session['state'] = '' # reset session state to prevent re-use

    # Okay to store this in a local variable, encrypt if it's going to client
    # machine or database. Treat as a password.
    session['microsoft_token'] = (response['access_token'], '')
    # Store the token in another session variable for easy access
    session['access_token'] = response['access_token']
    me_response = msgraphapi.get('me')
    me_data = json.loads(json.dumps(me_response.data))
    username = me_data['displayName']
    email_address = me_data['userPrincipalName']
    session['alias'] = username
    session['userEmailAddress'] = email_address
    return redirect('main')

@app.route('/main')
def main():
    """Handler for main route."""
    if session['alias']:
        username = session['alias']
        email_address = session['userEmailAddress']
        global article
        article = news_scraper.getRandomArticle(news)
        articleTitle = news_scraper.returnArticleTitle(article)
        articleText = news_scraper.returnArticleText(article)
        articleAuthor = news_scraper.returnArticleAuthors(article)
        articleImage = news_scraper.returnArticleImage(article)
        return render_template('main.html', article_title=articleTitle, article_text=articleText, article_author=articleAuthor, article_image=articleImage)
    else:
        return render_template('main.html')

@app.route('/send_mail')
def send_mail(email_address, name):
    """Handler for send_mail route."""
    response = call_sendmail_endpoint(session['access_token'], name, email_address)
    if response == 'SUCCESS':
        show_success = 'true'
        show_error = 'false'
    else:
        print(response)
        show_success = 'false'
        show_error = 'true'

    session['pageRefresh'] = 'false'


@msgraphapi.tokengetter
def get_token():
    """Return the Oauth token."""
    return session.get('microsoft_token')

def call_sendmail_endpoint(access_token, name, email_address):
    """Call the resource URL for the sendMail action."""
    send_mail_url = 'https://graph.microsoft.com/v1.0/me/microsoft.graph.sendMail'

    # set request headers
    headers = {'User-Agent' : 'python_tutorial/1.0',
               'Authorization' : 'Bearer {0}'.format(access_token),
               'Accept' : 'application/json',
               'Content-Type' : 'application/json'}

    # Use these headers to instrument calls. Makes it easier to correlate
    # requests and responses in case of problems and is a recommended best
    # practice.
    request_id = str(uuid.uuid4())
    instrumentation = {'client-request-id' : request_id,
                       'return-client-request-id' : 'true'}
    headers.update(instrumentation)

    # Create the email that is to be sent via the Graph API
    email = {'Message': {'Subject': 'I think you would like this article.',
                         'Body': {'ContentType': 'HTML',
                                  'Content': render_template('email.html', Friendname=name, SenderName=session['alias'], article_url=article.url)},
                         'ToRecipients': [{'EmailAddress': {'Address': email_address}}]
                        },
             'SaveToSentItems': 'true'}

    response = requests.post(url=send_mail_url,headers=headers,data=json.dumps(email),verify=False,params=None)
    if response.ok:
        return 'SUCCESS'
    else:
        return '{0}: {1}'.format(response.status_code, response.text)

@app.route('/submit')
def submit():
    takePic()
    data_blob = scoreImage()
    emo_1, val_1, emo_2, val_2 = parseScore(data_blob)
    val_1 = '{:2.0f}'.format(val_1*100)
    val_2 = '{:2.0f}'.format(val_2*100)
    title = article.title
    graph_blob = getPeople()
    global friends_name
    global friends_email
    friends_name = dict()
    friends_email = dict()
    i = 0
    for item in graph_blob['value']:
        
        name = item['displayName']
        email = item['scoredEmailAddresses'][0]['address']
        friends_name[str(i)] = name
        friends_email[str(i)] = email
        i = i+1
    if data_blob['happiness'] > 0.3:
        return render_template('results.html', emo_1=emo_1, val_1=val_1, emo_2=emo_2, val_2=val_2, friends_name=friends_name, friends_email=friends_email)
    else:
        return redirect('/main')        

def getPeople():

    me_response = msgraphapi.get('me/people')
    friends = json.loads(json.dumps(me_response.data))
    return friends

@app.route('/spam')
def spam():
    for key in friends_email.keys():
        print(key, friends_email[key])
        time.sleep(0.1)
        send_mail(friends_email[key], friends_name[key])

    return redirect('/main')