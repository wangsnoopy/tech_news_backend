import feedparser
import json
from pymongo import MongoClient
import os

# Load MongoDB URI from environment variable
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['tech_news_db']
articles_collection = db['articles']

# Function to fetch and convert RSS feed to JSON
def fetch_rss_to_json(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    
    # Extract relevant data from the RSS feed
    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary,
            'published': entry.published
        }
        articles.append(article)

    # Insert articles into MongoDB
    if articles:
        articles_collection.insert_many(articles)
    
    return articles

if __name__ == "__main__":
    rss_url = "https://news.ycombinator.com/rss"
    articles = fetch_rss_to_json(rss_url)
    print(f"Fetched and inserted {len(articles)} articles into MongoDB.")