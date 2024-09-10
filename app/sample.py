from pymongo import MongoClient

# MongoDB connection URI
mongo_uri = "your_mongo_connection_string"  # Replace with your MongoDB URI
client = MongoClient(mongo_uri)

# Connect to the database
db = client['tech_news_db']

# Insert some sample categories
categories_collection = db['categories']
categories_collection.insert_many([
    {"name": "AI/ML"},
    {"name": "Cloud Computing"},
    {"name": "Cybersecurity"}
])
print("Categories inserted!")

# Insert some sample articles
articles_collection = db['articles']
articles_collection.insert_many([
    {"title": "AI in 2024", "content": "The future of AI in 2024..."},
    {"title": "Cloud Computing Trends", "content": "Cloud computing is evolving..."},
    {"title": "Cybersecurity Insights", "content": "Top cybersecurity tips..."}
])
print("Articles inserted!")