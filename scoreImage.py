#####Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, sys, json
import numpy as np
def scoreImage():

    headers = {
        # Request headers. Replace the placeholder key below with your subscription key.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'db6977735f054bc293e38a0986c563eb',
    }

    params = urllib.parse.urlencode({
    })

    # Replace the example URL below with the URL of the image you want to analyze.
    body = "{ 'url': 'https://raw.githubusercontent.com/davidemily/testPics/master/photo.bmp' }"
    #body = "{ 'url': 'http://craftycat3.ddns.net/photos/download.jpg' }"

    try:
        # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
        #   URL below with "westcentralus".
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data)
        data = data[0]['scores']
        return data
        conn.close()
    except Exception as e:
        print(e.args)
    ####################################

def parseScore(json_blob):

    key_list = np.asarray([key for key in json_blob.keys()])
    value_list = np.asarray([json_blob[key_list[i]] for i in range(len(key_list))])
    top_2_index = np.argsort(value_list)[-2:]
    top_2_lists = list(key_list[top_2_index])+list(value_list[top_2_index])
    emo_1, val_1, emo_2, val_2 = top_2_lists[1], top_2_lists[3], top_2_lists[0], top_2_lists[2]
    return emo_1, val_1, emo_2, val_2



if __name__=='__main__':
    test = scoreImage()
