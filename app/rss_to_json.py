import feedparser
import os
from pymongo import MongoClient
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Load MongoDB URI from environment variable
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['tech_news_db']
articles_collection = db['articles']
products_collection = db['products']

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
        for article in articles:
            if not articles_collection.find_one({"link": article['link']}):  # Check if the article already exists
                articles_collection.insert_one(article)
    
    return articles

# Function to fetch and convert RSS feed for products
def fetch_products_to_json(feed_url):
    feed = feedparser.parse(feed_url)
    products = []
    
    # Extract relevant data from the RSS feed
    for entry in feed.entries:
        product = {
            'guid': entry.get('guid'),
            'url': entry.get('link'),
            'title': entry.get('title'),
            'content_html': entry.get('content_html', ''),
            'date_published': entry.get('published'),
            'author': entry.get('author') if isinstance(entry.get('author'), str) else entry.get('author', {}).get('name', '')
        }
        products.append(product)

    # Insert products into MongoDB
    if products:
        for product in products:
         # Check if the product already exists
            products_collection.insert_one(product)
    
    return products

# if not mongo_uri:
#     raise Exception("MongoDB URI not set in environment variables")

# print(f"Connecting to MongoDB at: {mongo_uri}")
# client = MongoClient(mongo_uri)
# db = client['tech_news_db']