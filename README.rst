FeedRSS reader Python
========

RSS feed reader for Python 3.

Features:

* Support for RSS, Atom and JSON feeds
* Background synchronization
* Caching and resizing of image embedded in feeds
* Removal of tracking pixels
* Grouping of feeds with tags
* Multi-users

Hosted service
--------------

* The interface is locally hosted.
* Port 8000 -- localhost

Development guide
-----------------

Feed reader is a typical Flask project, anyone familiar with Flask will feel
right at home. It requires:

* Python 3.7+
* SQLAlchemy database
* BackgroundScheduler for background tasks

Quickstart::
    from the console
        * git clone https://github.com/alejobastidas/FeedRSS_reader_Python.git
        * cd FeedRSS_reader_Python/
        * python3 -m venv venv
        * source venv/bin/activate
        * pip install -e .[dev]
        * python3 run.py
        
    Web browser:
        * http://127.0.0.1:5000/home
        * http://localhost:5000/home

