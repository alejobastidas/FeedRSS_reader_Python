from flask import render_template, url_for, flash, redirect, request, abort
from feed_reader.forms import RegistrationForm, LoginForm
from feed_reader.models import User, Source, Article
from time import mktime
from datetime import datetime
from feed_reader import app, db, bcrypt
from feed_reader.rssfeed import parse, get_source, get_articles
from flask_login import login_user, current_user, logout_user, login_required
import re, logging


@app.route("/",  methods=['GET', 'POST'])
@app.route("/home",  methods=['GET', 'POST'])
@login_required
def home():
    url_rss = request.form.get('url')
    if url_rss != None:
        if re.search(r"rss", url_rss):
            parsed = parse(url_rss)
            source_rss = get_source(parsed)
            source_val = Source.query.filter_by(user_id=current_user.id).all()
            source_list = []
            for val in source_val:
                source_list.append(val.title)

            if (source_rss['title'] in source_list):
                flash('You are already subscribed to this Feed!', 'info')
            else:
                articles_rss = get_articles(parsed)
                source = Source(title=source_rss['title'], subtitle=source_rss['subtitle'], link=source_rss['link'], user_id=current_user.id, feed=url_rss)
                db.session.add(source)
                db.session.commit()

                source_id = Source.query.filter_by(user_id=current_user.id)

                for article in articles_rss:
                    title=article['title']
                    body=article['summary']
                    link=article['link']
                    guid=article['id']
                    published=article['published']
                    published=datetime.fromtimestamp(mktime(published))

                    articles = Article(title=title, body=body, link=link, guid=guid, date_published=published ,source_id=source.id, user_id=current_user.id)
                    db.session.add(articles)
                    db.session.commit()
            sources = Source.query.filter_by(user_id=current_user.id).all()
        else: 
            sources = Source.query.filter_by(user_id=current_user.id).all()
            flash('Enter a valid Feed!', 'danger')
    else: 
        sources = Source.query.filter_by(user_id=current_user.id).all()

    return render_template('home.html', sources=sources)

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
    articles = Article.query.filter_by(user_id=current_user.id).all()
    return render_template('account.html', title='Account', articles=articles)

@app.route("/delete/<id>/", methods = ['GET', 'POST'])
@login_required
def delete(id):
    articles = Article.query.filter_by(user_id=current_user.id, source_id=id).all()
    
    for article in articles:
        db.session.delete(article)
        db.session.commit()

    sources = Source.query.get(id)
    db.session.delete(sources)
    db.session.commit()

    return redirect(url_for('home'))

def update():
    users = User.query.filter_by().all()
    for user in users:
        sources = Source.query.filter_by(user_id=user.id).all()
        for source in sources:
            articles = Article.query.filter_by(user_id=user.id, source_id=source.id).all()
            articles_list = []
            for val in articles:
                    articles_list.append(val.title)
            parsed = parse(source.feed)
            n=0
            while parsed.status != 200 or n>3:
                n+=1
                if n==3:
                    print('Feed not available')
                    LOG_FILENAME = 'logging_update.txt'
                    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,)
                    logging.error('Feed ' + str(source.title) + ' not available for ' + str(user.username))
            else:
                articles_up = get_articles(parsed)
                if articles_up[0]['title'] in articles_list:
                    print('Not Update')
                else:
                    for article in articles:
                        db.session.delete(article)
                        db.session.commit()

                    for article in articles_up:
                        title=article['title']
                        body=article['summary']
                        link=article['link']
                        guid=article['id']
                        published=article['published']
                        published=datetime.fromtimestamp(mktime(published))

                        articles = Article(title=title, body=body, link=link, guid=guid, date_published=published, source_id=source.id, user_id=user.id)
                        db.session.add(articles)
                        db.session.commit()
                    print('UPDATED')
                    LOG_FILENAME = 'logging_update.txt'
                    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,)
                    logging.info('Feed ' + str(source.title) + ' updated for ' + str(user.username))
