import unittest
from flask_login import current_user
from flask import request
from base import BaseTestCase
from feed_reader import bcrypt
from feed_reader.models import User, Source, Article
from feed_reader import rssfeed, routes, app, db

class UserModelTestCase(BaseTestCase):

    #PARSER TEST
    def test_parser(self):
        parsed = rssfeed.parse('https://www.eltiempo.com/rss/opinion.xml')
        self.assertEqual(parsed['feed']['title'], 'EL TIEMPO.COM - Opinión')

    #SOURCE TEST
    def test_source(self):
        parsed = rssfeed.parse('https://www.eltiempo.com/rss/opinion.xml')
        source = rssfeed.get_source(parsed)
        self.assertIn('link' and 'title' and 'subtitle', source)
    
    #ARTICLES TEST
    def test_articles(self):
        parsed = rssfeed.parse('https://www.eltiempo.com/rss/opinion.xml')
        articles = rssfeed.get_articles(parsed)
        self.assertIn('id' and 'link' and 'title' and 'summary' and 'published', articles[0])

    #REGISTER TEST
    def test_user_registration(self):
        response = self.client.post('/register', data=dict(
            username='alejo', email='alejo@bastidas.com',
            password='python', confirm='python'
        ), follow_redirects=True)
        self.assertIn(b'Join Today', response.data)
        user = User.query.filter_by(email='alejo@bastidas.com').first()
    
    #LOGIN TEST
    def test_login(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Log In' in response.get_data(as_text=True))

        response = self.client.post('/login', 
                                    data=dict(email='alejo@bastidas.com', password='python', 
                                    submit=True), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Log' in response.get_data(as_text=True))
    
    #HOME TEST
    def test_home(self):
        response = self.client.get('/home', follow_redirects=True, content_type='html/text')
        self.assertEqual(response.status_code, 200)

        
if __name__ == '__main__':
    unittest.main()