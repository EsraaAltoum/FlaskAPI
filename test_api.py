import unittest
import json
import app

BASE_URL = "http://127.0.0.1:5000/api/"
PING_RESPONSE = {"success": "true"}
TAG_ERROR_RESPONSE = {"error": "Tags parameter is required"}
SORT_BY_ERROR_RESPONSE = {"error": "sortBy parameter is invalid"}
DIRECTION_ERROR_RESPONSE = {"error": "direction parameter is invalid"}


class Tests(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True

    def test_ping(self):
        response = self.app.get(BASE_URL + "ping")
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(data, PING_RESPONSE) 
    
    def test_posts_no_params(self):
        response = self.app.get(BASE_URL + "posts")
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 400) 
        self.assertEqual(data, TAG_ERROR_RESPONSE) 
    
    def test_posts_invalid_sort(self):
        response = self.app.get(BASE_URL + "posts?tags=tech&sortBy=weird")
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 400) 
        self.assertEqual(data, SORT_BY_ERROR_RESPONSE)

    def test_posts_invalid_direction(self):
        response = self.app.get(BASE_URL + "posts?tags=tech&direction=weird")
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 400) 
        self.assertEqual(data, DIRECTION_ERROR_RESPONSE)

    def test_posts_single_tag(self):
            response = self.app.get(BASE_URL + "posts?tags=tech")
            data = json.loads(response.get_data())
            self.assertEqual(response.status_code, 200) 
            with open("tests/response_jsons/single_tag_response.json") as f:
                self.assertEqual(data, json.load(f))
    
    def test_posts_multiple_tags(self):
            response = self.app.get(BASE_URL + "posts?tags=tech,art,history")
            data = json.loads(response.get_data())
            self.assertEqual(response.status_code, 200) 
            with open("tests/response_jsons/multiple_tags_response.json") as f:
                self.assertEqual(data, json.load(f))
    
    def test_posts_valid_sort(self):
            response = self.app.get(BASE_URL + "posts?tags=tech&sortBy=popularity")
            data = json.loads(response.get_data())
            self.assertEqual(response.status_code, 200) 
            with open("tests/response_jsons/sort_by_popularity_response.json") as f:
                self.assertEqual(data, json.load(f))
    
    def test_posts_valid_direction(self):
            response = self.app.get(BASE_URL + "posts?tags=tech&direction=desc")
            data = json.loads(response.get_data())
            self.assertEqual(response.status_code, 200) 
            with open("tests/response_jsons/direction_descending_response.json") as f:
                self.assertEqual(data, json.load(f))

if __name__ == "__main__":
    unittest.main()
