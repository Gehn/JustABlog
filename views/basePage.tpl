<!DOCTYPE html>
<html>
	<head>
		<link href='http://fonts.googleapis.com/css?family=Michroma' rel='stylesheet' type='text/css'>
		<style>
			.title
			{
				font-family: 'Michroma', sans-serif;
				position:absolute;
				top:10px;
				left:240px;
				font-weight:bold;
				font-size:350%;
				text-decoration:none;
				color:#000;
				white-space:nowrap;
			}
			.subTitle
			{
				font-family: 'Michroma', sans-serif;
				position:absolute;
				top:62px;
				left:346px;
				font-weight:bold;
				font-size:250%;
				text-decoration:none;
				color:#000;
				white-space:nowrap;

			}

			.articleTitle
			{
				font-family: 'Michroma', sans-serif;
				font-weight:bold;
				font-size:140%;
			}
			.content
			{
				font-family: 'Michroma', sans-serif;
				position:absolute;
				top:200px;
				left:240px;
				margin-right:50px;
			}

			.index
			{
				position:fixed;
				top:150px;
				left:40px;
				border-right: 1px solid #bbb;

			}
			.indexTitle
			{
				font-family: 'Michroma', sans-serif;
				font-weight:bold;
				font-size:140%;
				text-decoration:none;
				color:#000;
			}
			.indexEntry
			{
				font-family: 'Michroma', sans-serif;
				font-size:100%;
				color:#000;
			}
			.tab
			{
				padding-left:5em
			}

		</style>
	</head>
	<body>
		<a class="title" href=/>{{blog.title}}</a>
		<a class="subTitle" href=/>{{blog.sub_title}}</a>
		<div class="index">
			<a class="indexTitle" href=/>Recent</a> <br>
			{% for article in blog.getRecentArticles(): %}
				<a class="indexEntry" href={{article.web_path}}>{{article.title}}</a> <br>
			{% endfor %}

			<br>
			<a class="indexTitle" href=/category>Categories</a> <br>
			{% for category in blog.getCategories(): %}
				<a class="indexEntry" href=/category/{{category}}>{{category}}</a> <br>
			{% endfor %}

			<br>
			<a class="indexTitle" href=/tag>Tags</a> <br>
			{% for tag in blog.getTags(): %}
				<a class="indexEntry" href=/tag/{{tag}}>{{tag}}</a> <br>
			{% endfor %}

		</div>
		<div class="content">
			{% block content %}
				{{content}}
			{% endblock %}
		</div>
	</body>
</html>
