from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
# Create the Flask app
app = Flask(__name__)

# MongoDB configuration
mongo_uri = os.getenv("MONGO_URI")
# Establishes the connection between your Flask application and the MongoDB
# MongoClient allows Flask application to read, write, and manage data in MongoDB instance
client = MongoClient(mongo_uri)

# Database name
db = client['tech_news_db']

# Import routes after creating the app and db connection
from app import routes