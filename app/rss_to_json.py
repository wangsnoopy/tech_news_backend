import feedparser
import os
from pymongo import MongoClient
import app.beautiful_soup_data as bsd
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Load MongoDB URI from environment variable
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['tech_news_db']
articles_collection = db['articles']
products_collection = db['products']
tools_collection = db['tools']


# Function to fetch and convert RSS feed to JSON for news
def fetch_rss_to_json(feed_url):
    # Clear the existing data in the collection
    articles_collection.delete_many({})  # Delete all previous articles

    feed = feedparser.parse(feed_url)
    articles = []
    
    # Extract relevant data from the RSS feed
    for entry in feed.entries:
        icon_url = bsd.fetch_icon_url(entry.link)
        article = {
            'title': entry.title,
            'link': entry.link,
            'icon_url': icon_url,
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
    # Clear the existing data in the collection
    products_collection.delete_many({})  # Delete all previous products

    feed = feedparser.parse(feed_url)
    products = []
    
    # Extract relevant data from the RSS feed
    for entry in feed.entries:
        icon_url = bsd.fetch_product_icon_url(entry.link)
        tag_line = bsd.fetch_tagline(entry.link)
        description = bsd.fetch_descriptions(entry.link)
        if not icon_url:
            icon_url = icon_url = bsd.fetch_icon_url(entry.link)
        product = {
            'guid': entry.get('guid'),
            'url': entry.get('link'),
            'title': entry.get('title'),
            'date_published': entry.get('published'),
            'author': entry.get('author') if isinstance(entry.get('author'), str) else entry.get('author', {}).get('name', ''),
            'icon_url': icon_url,
            'tag_line': tag_line,
            'description': description
        }
        products.append(product)

    # Insert products into MongoDB
    if products:
        for product in products:
         # Check if the product already exists
            products_collection.insert_one(product)
    
    return products


# Function to fetch and convert RSS feed for tools
def fetch_tools_to_json(feed_url):
    # Clear the existing data in the collection
    tools_collection.delete_many({})  # Delete all previous tools
    
    feed = feedparser.parse(feed_url)
    tools = []
    
    # Extract relevant data from the RSS feed
    for entry in feed.entries:
        tool = {
            'guid': entry.get('guid'),
            'url': entry.get('link'),
            'title': entry.get('title'),
            'content_html': entry.get('content_html', ''),
            'date_published': entry.get('published'),
            'author': entry.get('author') if isinstance(entry.get('author'), str) else entry.get('author', {}).get('name', '')
        }
        tools.append(tool)

    # Insert products into MongoDB
    if tools:
        for tool in tools:
         # Check if the product already exists
            tools_collection.insert_one(tool)
    
    return tools