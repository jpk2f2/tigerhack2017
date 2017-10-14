import requests
import newspaper
import random

#bbc_paper = newspaper.build('http://www.cnn.com')

# grab an article
#article = bbc_paper.articles[0]
#article.download()
#article.parse()
#print(article.text)

def buildArticleBase(address):
	articleList = newspaper.build(address)
	return articleList

def getFirstArticle(listData):
	article = listData.articles[0]
	return article

#does not work, don't use
def getRandomArticle(listData):
	#num = getNumArticles(listData)
	#x = random.randint(0,num)
	#article = listData.articles[x]
	#return article
        x = random.choice(listData.articles)
        return x

def  returnArticleText(article):
	article.download()
	article.parse()
	return(article.text)

def printArticleText(article):
	article.download()
	article.parse()
	print(article.text)

#doesn't appear to work, don't use	
def getNumArticles(listData):
	i = len(listData.articles)
	return i
