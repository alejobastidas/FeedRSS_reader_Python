from feed_reader import rssfeed
import re

def validate_url(url):
    if re.search(r"rss", url):
        parsed = rssfeed.parse(url)
        feed = parsed['feed']
        entries = parsed['entries'][0]
        if 'title' and 'link' and 'subtitle' in feed:
            if 'id' and 'link' and 'title' and 'summary' and 'published_parsed' in entries:
                return True
