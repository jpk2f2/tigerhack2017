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
	articleList = newspaper.build(address, memoize_articles = False, MIN_WORD_COUNT = 100, fetch_images = True)
	return articleList

def getFirstArticle(listData):
	article = listData.articles[1]
	return article

#does not work, don't use
def getRandomArticle(listData):
	#num = getNumArticles(listData)
	#x = random.randint(0,num)
	#article = listData.articles[x]
	#return article
    x = random.choice(listData.articles)
    return x

def returnArticleText(article):
	article.download()
	article.parse()
	return article.text

def returnArticleImage(article):
	article.download()
	article.parse()
	return article.top_image


def returnArticleUrl(article):
	article.download()
	article.parse()
	return article.url

def returnArticleTitle(article):
	article.download()
	article.parse()
	return article.title

def returnArticleAuthors(article):
	article.download()
	article.parse()
	author_list = article.authors
	return "; ".join(author_list)

def printArticleText(article):
	article.download()
	article.parse()
	print(article.text)

#doesn't appear to work, don't use	
def getNumArticles(listData):
	numArticles = len(listData.articles)
	return numArticles
