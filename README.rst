FeedRSS reader Python
========

RSS feed reader for Python 3.

Features:

* Support for RSS
* Allow new users
* Background synchronization
* Review of own feeds by registered users
* Log reports
* Multi-users

Hosted service
--------------

* The interface is locally hosted.
* Port 5000 -- localhost

Development guide
-----------------

Feed reader is a typical Flask project, anyone familiar with Flask will feel
right at home. It requires:

* Python 3.6+
* Flask
* SQLAlchemy database
* BackgroundScheduler for background tasks

Quickstart::
    from the console
        * git clone https://github.com/alejobastidas/FeedRSS_reader_Python.git
        * cd FeedRSS_reader_Python/
        * python3 -m venv venv
        * source venv/bin/activate
        * Make sure to install the Python libraries and package using:
                * pip3 install -r requirements.txt
        * python3 run.py
        
    Web browser:
        * http://127.0.0.1:5000/home
        * http://localhost:5000/home

