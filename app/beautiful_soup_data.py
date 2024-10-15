from bs4 import BeautifulSoup
import requests
import json
import pymongo
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
tools_collection = db['tools']

def fetch_tools_data_to_json():
    # Scrape GitHub Trending page
    url = 'https://github.com/trending?since=weekly'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Parse the title and summary of each repository
    repositories = []

    for repo in soup.find_all('article', class_='Box-row'):
        # Extract title
        title_tag = repo.find('h2', class_='h3 lh-condensed')
        title = title_tag.text.strip().replace("\n", "").replace(" ", "")  # Clean title

        # Extract summary
        summary_tag = repo.find('p', class_='col-9 color-fg-muted my-1 pr-4')
        summary = summary_tag.text.strip() if summary_tag else "No description provided."

        # Create repository object
        repository = {
            'title': title,
            'summary': summary
        }

        # Insert repository into MongoDB if it doesn't already exist
        if not tools_collection.find_one({"title": title}):  # Check if the repository already exists
            tools_collection.insert_one(repository)
            repositories.append(repository)

    return repositories
