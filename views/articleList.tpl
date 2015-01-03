{% extends "basePage.tpl" %}

{% block content %}

{% for article in article_list[:20]: %}
{%	set body = article.body[:1000] %}
	<div class="articleTitle"><span><a href={{article.web_path}}>{{article.title}}</a></span></div>
		{{body}}
	<br>
{% endfor %}

{% endblock %}
