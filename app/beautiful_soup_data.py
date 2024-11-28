from bs4 import BeautifulSoup
import requests
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

# Get tools data
def fetch_tools_data_to_json():
    tools_collection.delete_many({})
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

        # Extract star count
        star_tag = repo.find('a', href=lambda href: href and '/stargazers' in href)
        stars = star_tag.text.strip().replace(",", "") if star_tag else "0"

        # Extract fork count by locating the fork icon and finding the next sibling
        fork_tag = repo.find('a', href=lambda href: href and '/forks' in href)
        forks = fork_tag.text.strip().replace(",", "") if fork_tag else "0"

        # Extraxt which programing language
        language_tag = repo.find('span', itemprop='programmingLanguage')
        language = language_tag.text.strip() if language_tag else "Unknown"

        # Extract repository link
        link_tag = repo.find('a', href=True, class_='Link')
        link = f"https://github.com{link_tag['href']}" if link_tag else "No link provided"

        # Create repository object
        repository = {
            'title': title,
            'summary': summary,
            'stars': int(stars),
            'forks': int(forks),
            'language': language,
            'link': link
        }

        # Insert repository into MongoDB if it doesn't already exist
        if not tools_collection.find_one({"title": title}):  # Check if the repository already exists
            tools_collection.insert_one(repository)
            repositories.append(repository)

    return repositories

# Function to get the icon url from the webpage
def fetch_icon_url(page_url):
    try:
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            icon_tag = soup.find("link", rel="icon") or soup.find("link", rel="shortcut icon")
            if icon_tag and icon_tag.get("href"):
                icon_url = icon_tag["href"]
                # Handle relative URLs
                if icon_url.startswith('/'):
                    return page_url.rstrip('/') + icon_url
                return icon_url
        return None
    except requests.RequestException as e:
        print(f"Failed to fetch icon for {page_url}: {e}")
        return None

# products icon
def fetch_product_icon_url(page_url):
    try:
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for an <img> tag first
            img_tag = soup.find("img", class_="relative z-0 rounded")
            if img_tag:
                # Prefer srcset if available; fallback to src
                icon_url = img_tag.get("srcset") or img_tag.get("src")
                
                # If srcset exists, get the first URL (before the first space)
                if icon_url and " " in icon_url:
                    icon_url = icon_url.split()[0]
                
                return icon_url
            
            # If no <img> tag is found, then go to the cur link to get the web icon

        return None
    except requests.RequestException as e:
        print(f"Failed to fetch icon for {page_url}: {e}")
        return None
    
# product tag line
def fetch_tagline(page_url):
    try:
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the <h2> tag with the specified class
            tagline_tag = soup.find("h2", class_="text-24 font-light text-light-gray styles_tagline__Mhn2j")
            if tagline_tag:
                return tagline_tag.text.strip()  # Extract and clean up the text content
            
            # If no matching tag is found
            print("No matching <h2> tag found.")
            return None

    except requests.RequestException as e:
        print(f"Failed to fetch tagline for {page_url}: {e}")
        return None
    
# fetch description
def fetch_descriptions(page_url):
    try:
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all <div> tags with the specified class
            description_tags = soup.find_all("div", class_="styles_htmlText__eYPgj text-16 font-normal text-dark-gray")
            descriptions = [tag.text.strip() for tag in description_tags]  # Extract and clean text from each tag
            
            return descriptions if descriptions else "No descriptions found."

    except requests.RequestException as e:
        print(f"Failed to fetch descriptions for {page_url}: {e}")
        return None