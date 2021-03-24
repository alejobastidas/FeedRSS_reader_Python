import feedparser

def parse(url):
    parsed = feedparser.parse(url)
    return parsed

def get_source(parsed):
    feed = parsed['feed']
    return {
        'link': feed['link'],
        'title': feed['title'],
        'subtitle': feed['subtitle'],
    }

def get_articles(parsed):
    articles = []
    entries = parsed['entries']
    for entry in entries:
        articles.append({
            'id': entry['id'],
            'link': entry['link'],
            'title': entry['title'],
            'summary': entry['summary'],
            'published': entry['published_parsed'],
        })
    return articles


