Installation Instructions
=========================

Development
-----------

Requirements:
(tested versions appear in parentheses)

* unix (OS X 10.9.3)
* Python (3.3.5)
* virtualenv (1.11.4)
* pip (1.5.4)
* bottle (0.12.7)
* uWSGI (2.0.4)
* SQLAlchemy (0.9.4)

Installation Instructions:

1.  Clone the repo.
2.  cd to the root of the cloned repo dir.
3.  cd src/server
4.  virtualenv develop
5.  pip install -U bottle
6.  pip install -U uwsgi
7.  pip install -U sqlalchemy
8.  source develop/bin/activate
9.  cd ../..
10. bin/install_client.sh
11. bin/start.sh

This will start a web server running on port 8000 that serves the static files
and the dynamic content.


Production
----------

Requirements:

* unix (Server uses CentOS release 5.8 (Final))
* Python 3
* virtualenv
* pip
* bottle
* uwsgi

Instructions:

TODO
