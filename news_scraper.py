import requests
import newspaper

bbc_paper = newspaper.build('http://www.cnn.com')

# grab an article
article = bbc_paper.articles[0]
article.download()
article.parse()
print(article.text)
