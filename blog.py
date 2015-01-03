# Embedded file name: blog.py
import os
import datetime
import string
import shelve
from collections import defaultdict
from bottle import route, run, template
from datetime import date
import shutil
import re
import urllib
import traceback
from utilities import Log
from transformations import Transform

class Article:
	"""
		This class describes an article object.  Contains all metadata and content.
	"""

	def __init__(self, path = None, body = None, title = None, date = None, category = None, tags = []):
		"""
			Initialize an article.  If a path is given, and a body is not,
			attempts to read the body from the path.
			Then attempts to parse any metadata (_title, _date, _category, _tags)
			from the body.
		
			:param path: The path the article is located at.
			:param body: The text content of the article, in HTML.
			:param title: The title of the article.
			:param date: The date the article was written.
			:param category: The category the article is in.
			:param tags: The list of tags assigned to the article.
		"""
		self.path = None
		self.web_path = None
		self.body = None
		self.title = None
		self.date = None
		self.category = None
		self.tags = []
		if path:
			self.path = path
			self.title = os.path.basename(path)
		if body:
			self.body = body
		elif path:
			with open(path) as f:
				self.body = f.read()
		if self.body:
			self.parse(self.body)
		if title:
			self.title = title
		if date:
			self.date = date
		if category:
			self.category = category
		if tags:
			self.tags = tags
		date_in_file = self.date
		if not self.date:
			self.date = datetime.date.today()
		if self.path and not date_in_file:
			try:
				with open(self.path, 'a') as f:
					f.write('<!--_date=%s;-->' % str(self.date))
			except IOError as e:
				self.date = datetime.date.fromtimestamp(os.path.getctime(self.path))

		Log('Created Article: ', self.path, ' : ', self.title, ' : ', self.date, ' : ', self.category, ' : ', self.tags)
		return

	def parse(self, body):
		"""
			Parse text (HTML) to use as the body of the article.
			Metadata is extracted, and the string transformed as described
			in transforms.py
		
			:param body: the string to use as the body.
		"""
		title_match = re.search('_title=([^;]*);', body)
		date_match = re.search('_date=([^;]*);', body)
		category_match = re.search('_category=([^;]*);', body)
		tags_match = re.search('_tags=([^;]*);', body)
		if title_match:
			self.title = title_match.group(1)
		if date_match:
			self.date = datetime.datetime.strptime(date_match.group(1).split(' ')[0], '%Y-%m-%d').date()
		if category_match:
			self.category = category_match.group(1)
		if tags_match:
			self.tags = [ tag.strip() for tag in tags_match.group(1).split(',') ]
		self.body = Transform(body)
		return self.body

	def setWebPath(self, path):
		"""
			Set the URL-valid path to be used to access this article
		
			:param path: the un-quoted path to use.
		"""
		self.web_path = urllib.quote(path)


class Blog:
	"""
		The primary blog class.
	
		Contains all articles and staged_articles, sorted in various ways.
	"""

	def __init__(self, cfg_path = './blog.ini'):
		"""
			Initialize a blog object.
		
			Reads title, sub_title, file_root and staging from config file.
		
			:param cfg_path: the config file for the blog.
		"""
		self.cfg_path = cfg_path
		self.title = 'DebugThePlanet'
		self.sub_title = 'A place to write about things.'
		self.file_root = './articles/'
		self.staging = './staging/'
		self.categories = defaultdict(list)
		self.tags = defaultdict(list)
		self.articles = {}
		self.staged_articles = {}
		self.articles_by_date = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : {})))
		try:
			self.loadConfig(cfg_path)
		except IOError as e:
			pass


	# TODO: Try doing this with configparser, but need to determine if 
	# Bottles claim of being python 3 compatible without deps is actually
	# true since it seems to rely on jinja2 which may not be in the 3 core libs.
	def loadConfig(self, cfg_path):
		"""
			Load various metadata from the config file.
			(title, sub_title, file_root, staging)
		
			:param cfg_path: The path to the config file.
		"""
		for line in open(cfg_path).readlines():
			try:
				parameter = line.split('=')[0].strip().lower()
				value = line.split('=')[1].strip()
				if parameter == 'title':
					self.title = value
				if parameter == 'sub_title':
					self.sub_title = value
				if parameter == 'file_root':
					self.file_root = value
				if parameter == 'staging':
					self.staging = value
			except IndexError as e:
				pass

	def deploy(self, staged_article = None):
		"""
			Deply from staging to prod.
			If no article is specified, deploys all.
		
			:param staged_article: The title or article instance of the article to deploy.
		"""
		deploy_count = 0
		for title, article in self.staged_articles.iteritems():
			if not staged_article or staged_article == title or staged_article == article:
				if 'TODO:' in article.body:
					Log('Deploy gate failed, TODO found.  (Article: %s)' % (title,))
					break
				try:
					os.makedirs(self.file_root)
				except OSError as e:
					pass

				shutil.move(article.path, self.file_root)
				article.path = os.path.join(self.file_root, os.path.basename(article.path))
				article.setWebPath('/articles/' + title)
				self.indexArticle(article)
				deploy_count += 1

		return deploy_count

	#TODO: should possibly condense these into a single ParseArticles/ParseArticle/Index chain? less clear though...
	def parseStagedArticles(self):
		"""
			Ingest all files in the staging directory as Articles.
		"""
		for dirpath, dirnames, filenames in os.walk(self.staging):
			for filename in filenames:
				try:
					self.parseStagedArticle(os.path.join(dirpath, filename))
				except Exception as e:
					Log('Failure parsing staged article: ' + filename)
					Log(traceback.format_exc())
					continue

		return self.staged_articles

	def parseStagedArticle(self, article_path):
		"""
			Ingest a single file as an Article,
			and index it.
		
			:param article_file: The article filename to ingest.
		"""
		Log('Parsing staged article: ' + article_path)
		article = Article(article_path)
		article.setWebPath('/staging/' + article.title)
		self.staged_articles[article.title] = article

	def parseArticles(self):
		"""
			Ingest all files in the articles directory as Articles.
		"""
		for dirpath, dirnames, filenames in os.walk(self.file_root):
			for filename in filenames:
				try:
					self.parseArticle(os.path.join(dirpath, filename))
				except Exception as e:
					Log('Failure parsing article: ' + filename)
					Log(traceback.format_exc())
					continue

		return self.articles

	def parseArticle(self, article_path):
		"""
			Ingest a single file as an Article,
			and index it.
		
			:param article_file: the article filename to ingest.
		"""
		Log('Parsing article: ' + article_path)
		article = Article(article_path)
		article.setWebPath('/articles/' + self.title)
		self.indexArticle(article)
		return article

	def indexArticle(self, article):
		"""
			Refresh the indexes for a given article, clearing out any
			stale data.  Original article creation date is preserved.
		
			:param article: The article object to index.
		"""
		if article.title in self.articles:
			old_article = self.articles[article.title]
			article.date = old_article.date
			if old_article.category:
				self.categories[old_article.category].remove(old_article)
			for tag in old_article.tags:
				self.tags[tag].remove(old_article)

		self.articles[article.title] = article
		if article.category:
			self.categories[article.category].append(article)
		for tag in article.tags:
			self.tags[tag].append(article)

		self.articles_by_date[article.date.year][article.date.month][article.date.day][article.title] = article

	def getRecentArticles(self, number_to_get = 10):
		"""
			Get number_to_get most recent articles.
		
			:param number_to_get: The number of articles to return.
		"""
		recent_articles = []
		years = list(self.articles_by_date.keys())
		years.reverse()
		for year in years:
			months = list(self.articles_by_date[year].keys())
			months.reverse()
			for month in months:
				days = list(self.articles_by_date[year][month].keys())
				days.reverse()
				for day in days:
					articles = sorted(self.articles_by_date[year][month][day].values(), key=lambda article: article.date)
					for article in articles:
						recent_articles.append(article)
						if len(recent_articles) > number_to_get:
							return recent_articles

		return recent_articles

	def getArticles(self):
		"""
			Get a list of all articles.
		"""
		return self.articles.values()

	def getArticle(self, article):
		"""
			Get an Article object of a given title,
			must have been parsed in prior.
		
			:param article: The title of the article to get.
		"""
		return self.articles[article]

	def getCategories(self):
		"""
			Get a list of all categories.
		"""
		return self.categories.keys()

	def getArticlesByCategory(self, category):
		"""
			Get all articles within a given category.
		
			:param category: The category to enumerate.
		"""
		if category in self.categories:
			return self.categories[category]
		return []

	def getTags(self):
		"""
			Get a list of all tags.
		"""
		return self.tags.keys()

	def getArticlesByTag(self, tag):
		"""
			Get all articles within a given tag.
			:param tag: The tag to enumerate.
		"""
		if tag in self.tags:
			return self.tags[tag]
		return []

	def getStagedArticles(self):
		"""
			Get a list of all staged articles.
		"""
		return self.staged_articles.values()

	def getStagedArticle(self, article):
		"""
			Get a staged Article object of a given title,
			must have been parsed in prior.
		
			:param article: the title of the article to get.
		"""
		return self.staged_articles[article]
