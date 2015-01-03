DebugTheBlog: A micro blog framework
====================================


To Run:
=======
python run.py [tests]


Version Info:
=============
Version 1.0


Requirements:
=============
Python 2.6-2.7 compatible (3 WIP, pending a potential bug in bottle)


To Configure:
=============
blog.ini in the running directory contains settings.  A different config file path can be specified at launch.

articles should be put in the running ./articles directory; this can be changed in the config file.
Similarly for staged articles and ./staging

The title and sub_title for the blog can be set in the config file as well. (simple title = foo format, newline deliniated)

Articles can get _title=foo; _date=yyyy-mm-dd; _category=foo; _tags=foo,bar; style metadata in HTML comments anywhere in their file.
These do not have to be defined.


API:
====
Articles may be deployed with /deploy/<staged article>, disallowed if there is a TODO: in the body.



