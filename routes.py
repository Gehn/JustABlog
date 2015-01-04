#!/usr/bin/env python3

import functools
import os
import string
import urllib

from blog import Blog
from bottle import route, run, template, jinja2_view, url, Jinja2Template, response
from utilities import Log




# ----- INITIALIZE THE BLOG ----- #

# I'm not sure I'm happy with this; but making it all static doesn't seem much better.
blog_instance = Blog()
blog_instance.parseArticles()
blog_instance.parseStagedArticles()

# ----- SET UP THE TEMPLATE ENGINE ----- #

Jinja2Template.defaults = {
    'url': url,
    'blog': blog_instance,
}

# ----- SET UP HELPER FUNCTIONS ----- #

# Convenience function to set up views from the right directory
view = functools.partial(jinja2_view, template_lookup=['views'])

def sanitize(callback):
	'''
		Make sure all arguments to the function are in the whitelist
		for characters, additionally unquotes the stringe.

		:param callback: The function to sanitize.
	'''
	def sanitized_callback(*args, **kwargs):
		#TODO: read from config?  It'd be nice but I don't imagine it changing much.
		whitelist = string.ascii_letters + string.digits + '_' + '-' + ' '

		sanitized_args = []
		sanitized_kwargs = {}

		for arg in args:
			if arg.__class__.__name__ == "str":
				sanitized_args.append(urllib.unquote(arg))
				for char in arg:
					if char not in whitelist:
						response.status = 303
						response.set_header('Location', '/error')
						Log("Invalid post character: %s" % (arg,))
						return {}

		for (key, value) in kwargs.items():
			if value.__class__.__name__ == "str":
				sanitized_kwargs[key] = urllib.unquote(value)
				for char in value:
					if char not in whitelist:
						response.status = 303
						response.set_header('Location', '/error')
						Log("Invalid post character: %s" % (value,))
						return {}

		return callback(*args, **kwargs)

	return sanitized_callback


def make_link(destination, text=None):
	'''
		Convenience function, generate the HTML for a link.

		:param destination: the location of the link.
		:param text: the alt text of the link. (default = destination)
	'''
	if not text:
		text = destination

	return "<a href=\"%s\">%s</a>" % (destination, text)

# ----- ROUTES ----- #

@route("/")
@sanitize
@view("articleList.tpl")
def root():
	blog_instance.parseArticles()
	recent_articles = blog_instance.getRecentArticles()
	return {'article_list': recent_articles}


@route("/articles/<post>")
@sanitize
@view("basePage.tpl")
def article(post):
	article = blog_instance.getArticle(post)

	return {'content': article.body}


@route("/staging")
@sanitize
@view("articleList.tpl")
def searchStagedArticles(post=None):
	blog_instance.parseStagedArticles()

	return {'article_list': blog_instance.getStagedArticles()}


@route("/staging/<post>")
@sanitize
@view("basePage.tpl")
def viewStagedArticle(post):
	staged_article = blog_instance.getStagedArticle(post)

	return {'content': staged_article.body}


@route("/deploy/<post>")
@sanitize
@view("basePage.tpl")
def viewStagedArticle(post):
	deploy_count = blog_instance.deploy(post)

	if deploy_count > 0:
		response.status = 303
		response.set_header('Location', '/articles/' + post)
		return {}

	response.status = 303
	response.set_header('Location', '/error')
	return {}


@route("/<year:int>")
@route("/<year:int>/<month:int>")
@route("/<year:int>/<month:int>/<day:int>")
@sanitize
@view("articleList.tpl")
def searchByDate(year, month=None, day=None):
	# Do the right thing no matter which parts of the date are given.
	if day:
		articles = blog_instance.articles_by_date[year][month][day].values()
	elif month:
		articles = []
		for day in blog_instance.articles_by_date[year][month]:
			articles += blog_instance.articles_by_date[year][month][day].values()
	else:
		articles = []
		for month in blog_instance.articles_by_date[year]:
			for day in blog_instance.articles_by_date[year][month]:
				articles += blog_instance.articles_by_date[year][month][day].values()

	return {"article_list": articles}


@route("/category/<category>")
@sanitize
@view("articleList.tpl")
def searchByCategory(category):
	articles = blog_instance.getArticlesByCategory(category)

	return {"article_list": articles}


@route("/category")
@sanitize
@view("basePage.tpl")
def searchtags():
	content = [make_link("/category/" + tag, tag) + "<br>" for tag in blog_instance.getCategories()]
	return {"content": "".join(content)}


@route("/tag/<tag>")
@sanitize
@view("articleList.tpl")
def searchByTag(tag):
	articles = blog_instance.getArticlesByTag(tag)

	return {"article_list": articles}


@route("/tag")
@sanitize
@view("basePage.tpl")
def searchTags():
	content = [make_link("/tag/" + tag, tag) + "<br>" for tag in blog_instance.getTags()]
	return {"content": "".join(content)}


@route("/error")
@sanitize
@view("basePage.tpl")
def searchTags():
	return {"content": "Something happened.  See server logs to find out what."}


def Run(config_path=None):
	'''
		Run the web server for the site specified by the routes in this module.

		:param config_path: Optional additional or alternate configuration file.
	'''
	if config_path:
		blog_instance.loadConfig(config_path)
	run(host='localhost', port=8080)


if __name__=="__main__":
	Run()
