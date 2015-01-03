import datetime
import unittest
import os

import blog
from utilities import LoggingOff


class ArticleInitializationTests(unittest.TestCase):
	def test_empty_initialize(self):
		article = blog.Article()

		self.assertEqual(article.title, None)
		self.assertEqual(article.body, None)
		self.assertEqual(article.path, None)
		self.assertEqual(article.web_path, None)
		self.assertEqual(article.category, None)
		self.assertEqual(article.tags, [])

		self.assertEqual(article.date.__class__, datetime.date)


	def test_initialize_with_parameters(self):
		test_body = "TESTBODY"
		test_title = "TESTTITLE"
		test_date = datetime.date.today()
		test_path = "TESTPATH"
		test_category = "TESTCATEGORY"
		test_tags = ["TESTTAG", "TESTTAG2"]

		article = blog.Article(path = test_path, body=test_body, title=test_title, date=test_date, category=test_category, tags=test_tags)

		self.assertEqual(article.title, test_title)
		self.assertEqual(article.body, test_body)
		self.assertEqual(article.path, test_path)
		self.assertEqual(article.web_path, None)
		self.assertEqual(article.category, test_category)
		self.assertEqual(article.tags, test_tags)
		self.assertEqual(article.date, test_date)

		
	def test_initialize_with_body_with_metadata(self):
		test_title = "TESTTITLE"
		test_date = datetime.date.today()
		test_path = "TESTPATH"
		test_category = "TESTCATEGORY"
		test_tags = ["TESTTAG", "TESTTAG2"]

		test_body = "TESTBODY"
		test_body += "<!--_title=%s;-->" % (test_title,)
		test_body += "<!--_date=%s;-->" % (str(test_date),)
		test_body += "<!--_category=%s;-->" % (test_category,)
		test_body += "<!--_tags=%s;-->" % (", ".join(test_tags),)

		article = blog.Article(body=test_body)

		self.assertEqual(article.title, test_title)
		self.assertEqual(article.body, test_body)
		self.assertEqual(article.path, None)
		self.assertEqual(article.web_path, None)
		self.assertEqual(article.category, test_category)
		self.assertEqual(set(article.tags), set(test_tags))

		self.assertEqual(article.date, test_date)


	def test_initialize_from_file(self):
		test_title = "TESTTITLE"
		test_date = datetime.date.today()
		test_path = "TESTPATH"
		test_category = "TESTCATEGORY"
		test_tags = ["TESTTAG", "TESTTAG2"]

		test_body = "TESTBODY"
		test_body += "<!--_title=%s;-->" % (test_title,)
		test_body += "<!--_date=%s;-->" % (str(test_date),)
		test_body += "<!--_category=%s;-->" % (test_category,)
		test_body += "<!--_tags=%s;-->" % (", ".join(test_tags),)


		test_path = "tests/articles/test_article"

		with open(test_path, 'w') as f:
			f.write(test_body)

		article = blog.Article(path=test_path)

		self.assertEqual(article.title, test_title)
		self.assertEqual(article.body, test_body)
		self.assertEqual(article.path, test_path)
		self.assertEqual(article.web_path, None)
		self.assertEqual(article.category, test_category)
		self.assertEqual(set(article.tags), set(test_tags))

		self.assertEqual(article.date, test_date)


	def test_initialize_from_file_with_overrides(self):
		test_title = "TESTTITLE"
		test_date = datetime.date.today()
		test_path = "TESTPATH"
		test_category = "TESTCATEGORY"
		test_tags = ["TESTTAG", "TESTTAG2"]

		test_body = "TESTBODY"
		test_body += "<!--_title=%s;-->" % (test_title,)
		test_body += "<!--_date=%s;-->" % (str(test_date),)
		test_body += "<!--_category=%s;-->" % (test_category,)
		test_body += "<!--_tags=%s;-->" % (", ".join(test_tags),)


		test_path = "tests/articles/test_article"

		with open(test_path, 'w') as f:
			f.write(test_body)

		override_test_title = "OVERRIDETESTTITLE"
		override_test_date = datetime.date.today()
		override_test_category = "OVERRIDETESTCATEGORY"
		override_test_tags = ["OVERRIDETESTTAG", "OVERRIDETESTTAG2"]

		article = blog.Article(path=test_path, title=override_test_title, date=override_test_date, category=override_test_category, tags=override_test_tags)

		self.assertEqual(article.title, override_test_title)
		self.assertEqual(article.body, test_body)
		self.assertEqual(article.path, test_path)
		self.assertEqual(article.web_path, None)
		self.assertEqual(article.category, override_test_category)
		self.assertEqual(set(article.tags), set(override_test_tags))

		self.assertEqual(article.date, override_test_date)



	def test_initialize_from_readonly_file_without_date(self):
		test_title = "TESTTITLE"
		test_date = datetime.date.today()
		test_path = "TESTPATH"
		test_category = "TESTCATEGORY"
		test_tags = ["TESTTAG", "TESTTAG2"]

		test_body = "TESTBODY"
		test_body += "<!--_title=%s;-->" % (test_title,)
		test_body += "<!--_category=%s;-->" % (test_category,)
		test_body += "<!--_tags=%s;-->" % (", ".join(test_tags),)


		test_path = "tests/articles/test_article_without_date"

		try:
			os.chmod(test_path, 0666)
		except:
			pass

		with open(test_path, 'w') as f:
			f.write(test_body)

		os.chmod(test_path, 0444)

		article = blog.Article(path=test_path)

		self.assertEqual(article.title, test_title)
		self.assertEqual(article.body, test_body)
		self.assertEqual(article.path, test_path)
		self.assertEqual(article.web_path, None)
		self.assertEqual(article.category, test_category)
		self.assertEqual(set(article.tags), set(test_tags))

		self.assertEqual(article.date.__class__, datetime.date)



	def test_set_web_path(self):
		test_web_path = "test/path"

		article = blog.Article()

		self.assertEqual(article.web_path, None)

		article.setWebPath(test_web_path)

		self.assertEqual(article.web_path, test_web_path)


	def test_parse_after_initialization(self):
		article = blog.Article()

		test_title = "TESTTITLE"
		test_date = datetime.date.today()
		test_path = "TESTPATH"
		test_category = "TESTCATEGORY"
		test_tags = ["TESTTAG", "TESTTAG2"]

		test_body = "TESTBODY"
		test_body += "<!--_title=%s;-->" % (test_title,)
		test_body += "<!--_date=%s;-->" % (str(test_date),)
		test_body += "<!--_category=%s;-->" % (test_category,)
		test_body += "<!--_tags=%s;-->" % (", ".join(test_tags),)

		article.parse(test_body)

		self.assertEqual(article.title, test_title)
		self.assertEqual(article.body, test_body)
		self.assertEqual(article.path, None)
		self.assertEqual(article.web_path, None)
		self.assertEqual(article.category, test_category)
		self.assertEqual(set(article.tags), set(test_tags))

		self.assertEqual(article.date, test_date)


class BlogInitializationTests(unittest.TestCase):
	def test_empty_initialization(self):
		blog_instance = blog.Blog()


	def test_initialization_with_config_file(self):
		test_title = "TESTTITLE"
		test_sub_title = "TESTSUBTITLE"
		test_article_dir = "./tests/articles"
		test_staging_root = "./tests/staging"

		cfg_file_body = ""
		cfg_file_body += "title = %s\n" % (test_title,)
		cfg_file_body += "sub_title = %s\n" % (test_sub_title,)
		cfg_file_body += "article_dir = %s\n" % (test_article_dir,)
		cfg_file_body += "staging_dir = %s\n" % (test_staging_root,)

		cfg_file_path = "./tests/test_cfg.ini"

		with open(cfg_file_path, 'w') as f:
			f.write(cfg_file_body)

		blog_instance = blog.Blog(cfg_file_path)

		self.assertEqual(blog_instance.title, test_title)
		self.assertEqual(blog_instance.sub_title, test_sub_title)
		self.assertEqual(blog_instance.article_dir, test_article_dir)
		self.assertEqual(blog_instance.staging_dir, test_staging_root)


	def test_parse_articles_empty_dir(self):
		blog_instance = blog.Blog()

		#FIXME: move this stuff to setUp()? (the creation stuff basically everywhere)
		empty_dir = "./tests/empty_dir"

		try:
			os.makedirs(empty_dir)
		except OSError as e:
			pass

		blog_instance.article_dir = empty_dir

		blog_instance.parseArticles()

		self.assertEqual(blog_instance.getArticles(), [])


	def test_parse_articles_dir(self):
		blog_instance = blog.Blog()

		populated_dir = "./tests/populated_dir"

		try:
			os.makedirs(populated_dir)
		except OSError as e:
			pass

		test_article_1 = "test_article_1"
		test_article_2 = "test_article_2"

		open(os.path.join(populated_dir, test_article_1), "w")
		open(os.path.join(populated_dir, test_article_2), "w")

		blog_instance.article_dir = populated_dir

		blog_instance.parseArticles()

		self.assertEqual(len(blog_instance.getArticles()), 2)
		self.assertEqual(blog_instance.getArticle(test_article_1).title, test_article_1)
		self.assertEqual(blog_instance.getArticle(test_article_2).title, test_article_2)


	def test_parse_staging_empty_dir(self):
		blog_instance = blog.Blog()

		empty_dir = "./tests/empty_dir"

		try:
			os.makedirs(empty_dir)
		except OSError as e:
			pass

		blog_instance.staging_dir = empty_dir

		blog_instance.parseStagedArticles()

		self.assertEqual(blog_instance.getStagedArticles(), [])


	def test_parse_staging_dir(self):
		blog_instance = blog.Blog()

		populated_dir = "./tests/populated_dir"

		try:
			os.makedirs(populated_dir)
		except OSError as e:
			pass

		test_article_1 = "test_article_1"
		test_article_2 = "test_article_2"

		open(os.path.join(populated_dir, test_article_1), "w")
		open(os.path.join(populated_dir, test_article_2), "w")

		blog_instance.staging_dir = populated_dir

		blog_instance.parseStagedArticles()

		self.assertEqual(len(blog_instance.getStagedArticles()), 2)
		self.assertEqual(blog_instance.getStagedArticle(test_article_1).title, test_article_1)
		self.assertEqual(blog_instance.getStagedArticle(test_article_2).title, test_article_2)


	def test_index_single_article(self):
		test_body = "TESTBODY"
		test_title = "TESTTITLE"
		test_date = datetime.date.today()
		test_path = "TESTPATH"
		test_category = "TESTCATEGORY"
		test_tags = ["TESTTAG", "TESTTAG2"]

		article = blog.Article(path = test_path, body=test_body, title=test_title, date=test_date, category=test_category, tags=test_tags)

		blog_instance = blog.Blog()

		blog_instance.indexArticle(article)

		self.assertEqual(set(blog_instance.getArticles()), set([article]))
		self.assertEqual(set(blog_instance.getRecentArticles()), set([article]))
		self.assertEqual(set(blog_instance.getArticlesByCategory(article.category)), set([article]))
		self.assertEqual(set(blog_instance.getCategories()), set([article.category]))
		self.assertEqual(set(blog_instance.getArticlesByTag(article.tags[0])), set([article]))
		self.assertEqual(set(blog_instance.getArticlesByTag(article.tags[1])), set([article]))
		self.assertEqual(set(blog_instance.getTags()), set(article.tags))


	def test_index_multiple_articles(self):
		test_body = "TESTBODY"
		test_title = "TESTTITLE"
		test_date = datetime.date.today()
		test_path = "TESTPATH"
		test_category = "TESTCATEGORY"
		test_tags = ["TESTTAG", "TESTTAG2"]

		test_body_2 = "TESTBODY2"
		test_title_2 = "TESTTITLE2"
		test_date_2 = datetime.date.today()
		test_path_2 = "TESTPATH2"
		test_category_2 = "TESTCATEGORY2"
		test_tags_2 = ["TESTTAG3", "TESTTAG4"]


		article = blog.Article(path = test_path, body=test_body, title=test_title, date=test_date, category=test_category, tags=test_tags)
		article2 = blog.Article(path = test_path_2, body=test_body_2, title=test_title_2, date=test_date_2, category=test_category_2, tags=test_tags_2)

		blog_instance = blog.Blog()

		blog_instance.indexArticle(article)
		blog_instance.indexArticle(article2)

		self.assertEqual(set(blog_instance.getArticles()), set([article, article2]))
		self.assertEqual(set(blog_instance.getRecentArticles()), set([article, article2]))
		self.assertEqual(set(blog_instance.getArticlesByCategory(article.category)), set([article]))
		self.assertEqual(set(blog_instance.getArticlesByCategory(article2.category)), set([article2]))
		self.assertEqual(set(blog_instance.getCategories()), set([article.category, article2.category]))
		self.assertEqual(set(blog_instance.getArticlesByTag(article.tags[0])), set([article]))
		self.assertEqual(set(blog_instance.getArticlesByTag(article.tags[1])), set([article]))
		self.assertEqual(set(blog_instance.getArticlesByTag(article2.tags[0])), set([article2]))
		self.assertEqual(set(blog_instance.getArticlesByTag(article2.tags[1])), set([article2]))
		self.assertEqual(set(blog_instance.getTags()), set(article.tags + article2.tags))


	def test_get_recent_no_articles(self):
		blog_instance = blog.Blog()

		self.assertEqual(blog_instance.getRecentArticles(), [])


	def test_get_recent_one_article(self):
		blog_instance = blog.Blog()

		article = blog.Article()
		article.title = "TESTTILE"

		blog_instance.indexArticle(article)

		self.assertEqual(blog_instance.getRecentArticles(), [article])


	def test_get_recent_many_articles(self):
		blog_instance = blog.Blog()

		article = blog.Article()
		article.title = "TESTTILE"
		article2 = blog.Article()
		article2.title = "TESTTILE2"
		article3 = blog.Article()
		article3.title = "TESTTILE3"

		article2.date = datetime.date(2014,1,1) 
		article3.date = datetime.date(2013,1,1) 

		blog_instance.indexArticle(article)
		blog_instance.indexArticle(article2)
		blog_instance.indexArticle(article3)

		self.assertEqual(blog_instance.getRecentArticles(), [article, article2, article3])


	def test_get_by_tag_no_tags(self):
		blog_instance = blog.Blog()

		self.assertEqual(blog_instance.getArticlesByTag("NotReal"), [])


	def test_get_by_tag_empty_tag(self):
		blog_instance = blog.Blog()

		article = blog.Article()
		article.title = "TESTTITLE"
		article.tags = ["tag"]

		blog_instance.indexArticle(article)

		self.assertEqual(blog_instance.getArticlesByTag("NotReal"), [])


	def test_get_by_tag_one_tag(self):
		blog_instance = blog.Blog()

		article = blog.Article()
		article.title = "TESTTITLE"
		article.tags = ["tag"]

		blog_instance.indexArticle(article)

		self.assertEqual(blog_instance.getArticlesByTag("tag"), [article])


	def test_get_by_tag_many_tags(self):
		blog_instance = blog.Blog()

		article = blog.Article()
		article.title = "TESTTITLE"
		article.tags = ["tag"]
		article2 = blog.Article()
		article2.title = "TESTTITLE2"
		article2.tags = ["tag2", "tag3"]
		article3 = blog.Article()
		article3.title = "TESTTITLE3"
		article3.tags = ["tag3"]

		blog_instance.indexArticle(article)
		blog_instance.indexArticle(article2)
		blog_instance.indexArticle(article3)

		self.assertEqual(blog_instance.getArticlesByTag("tag"), [article])
		self.assertEqual(blog_instance.getArticlesByTag("tag2"), [article2])
		self.assertEqual(set(blog_instance.getArticlesByTag("tag3")), set([article2, article3]))


	def test_get_by_category_no_categories(self):
		blog_instance = blog.Blog()

		self.assertEqual(blog_instance.getArticlesByCategory("NotReal"), [])


	def test_get_by_category_empty_category(self):
		blog_instance = blog.Blog()

		article = blog.Article()
		article.title = "TESTTITLE"
		article.category = "TESTCATEGORY"

		blog_instance.indexArticle(article)

		self.assertEqual(blog_instance.getArticlesByTag("NotReal"), [])


	def test_get_by_category_one_category(self):
		blog_instance = blog.Blog()

		article = blog.Article()
		article.title = "TESTTITLE"
		article.category = "TESTCATEGORY"

		blog_instance.indexArticle(article)

		self.assertEqual(blog_instance.getArticlesByCategory(article.category), [article])


	def test_get_by_category_many_categories(self):
		blog_instance = blog.Blog()

		article = blog.Article()
		article.title = "TESTTITLE"
		article.category = "TESTCATEGORY"
		article1 = blog.Article()
		article1.title = "TESTTITLE1"
		article1.category = "TESTCATEGORY"
		article2 = blog.Article()
		article2.title = "TESTTITLE2"
		article2.category = "TESTCATEGORY2"
		article3 = blog.Article()
		article3.title = "TESTTITLE3"
		article3.category = "TESTCATEGORY3"

		blog_instance.indexArticle(article)
		blog_instance.indexArticle(article1)
		blog_instance.indexArticle(article2)
		blog_instance.indexArticle(article3)

		self.assertEqual(set(blog_instance.getArticlesByCategory(article.category)), set([article, article1]))
		self.assertEqual(blog_instance.getArticlesByCategory(article2.category), [article2])
		self.assertEqual(blog_instance.getArticlesByCategory(article3.category), [article3])



def Main():
	LoggingOff()
	unittest.main()


if __name__ == "__main__":
	Main()
