import unittest
import requests # request library to make HTTP request to the Falsk API

BASE_URL_NEWS = "http://localhost:5001/newest"
BASE_URL_PRODUCTS = "http://localhost:5001/products"
BASE_URL_CATEGORIES = "http://localhost:5001/categories"
BASE_URL_SUBSCRIBE = "http://localhost:5001/subscribe"
BASE_URL_TOOLS = "http://localhost:5001/tool"

# Define a test case class that inherits from unittest.TestCase.
class TestFlaskAPI(unittest.TestCase):

    def test_get_news(self):
        # Send a GET request to the /newest route.
        response = requests.get(f"{BASE_URL_NEWS}")
        
        # Assert that the HTTP status code of the response is 200 (OK).
        self.assertEqual(response.status_code, 200, "Expected status code 200")
        # Assert that the response's Content-Type header is 'application/json'
        self.assertTrue(response.headers['Content-Type'] == 'application/json', "Response is not JSON")
        
        data = response.json()
        
        # Check if the response has the correct structure
        self.assertIn('title', data[0], "Response is missing 'title' field")
        self.assertIn('link', data[0], "Response is missing 'link' field")
        self.assertIn('summary', data[0], "Response is missing 'summary' field")
        self.assertIn('published', data[0], "Response is missing 'published' field")

    def test_get_products(self):
        response = requests.get(f"{BASE_URL_PRODUCTS}")
        
        # Check that the status code is 200
        self.assertEqual(response.status_code, 200, "Expected status code 200")
        
        # Check that the response is in JSON format
        self.assertTrue(response.headers['Content-Type'] == 'application/json', "Response is not JSON")
        
        data = response.json()
        
        # Check that the response contains at least one product
        self.assertIn('guid', data[0], "Response is missing 'guid' field")
        self.assertIn('url', data[0], "Response is missing 'url' field")
        self.assertIn('title', data[0], "Response is missing 'title' field")
        self.assertIn('content_html', data[0], "Response is missing 'content_html' field")
        self.assertIn('date_published', data[0], "Response is missing 'date_published' field")
        self.assertIn('author', data[0], "Response is missing 'author' field")
    
    def test_get_categories(self):
        response = requests.get(f"{BASE_URL_CATEGORIES}")
        
        # Check that the status code is 200
        self.assertEqual(response.status_code, 200, "Expected status code 200")
        
        # Check that the response is in JSON format
        self.assertTrue(response.headers['Content-Type'] == 'application/json', "Response is not JSON")
        
        data = response.json()

        self.assertIn('categories', data, "Response is missing 'categories' field")
    
    def test_post_subscribe(self):
        # Define the endpoint
        url = f"{BASE_URL_SUBSCRIBE}"

        # Test case 1: Valid subscription request
        valid_email = {"email": "test@example.com"}
        response = requests.post(url, json=valid_email)
        
        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201, "Expected status code 201 for valid subscription")
        # Assert that the response is in JSON format
        self.assertTrue(response.headers['Content-Type'] == 'application/json', "Response is not JSON")
        # Assert that the response contains the correct success message
        self.assertIn("Subscription successful!", response.json().get('message', ''), "Response message does not match expected value")
        
        # Test case 2: Missing email in the request body
        missing_email = {}
        response = requests.post(url, json=missing_email)
        
        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400, "Expected status code 400 for missing email")
        # Assert that the response contains the correct error message
        self.assertIn("Email is required", response.json().get('error', ''), "Response message does not match expected value for missing email")
        
        # Test case 3: Invalid email format
        invalid_email = {"email": "invalid-email"}
        response = requests.post(url, json=invalid_email)
        
        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400, "Expected status code 400 for invalid email format")
        # Assert that the response contains the correct error message
        self.assertIn("Invalid email format", response.json().get('error', ''), "Response message does not match expected value for invalid email")

        # the except code of the backend is 201/400/400 for the three test case