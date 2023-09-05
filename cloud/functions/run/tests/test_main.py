import unittest
import requests
from unittest.mock import Mock, patch
import os


class TestSynthesizeFunction(unittest.TestCase):

    def setUp(self):
        # Set up environment variable for testing
        os.environ['FLOWER_API_URL'] = 'http://test-flower.com'

    def tearDown(self):
        # Clean up environment variable after testing
        del os.environ['FLOWER_API_URL']

    @patch('main.requests.post')
    def test_synthesize_success(self, mock_post):
        # Define a mock response for requests.post
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'task-id': '649531ec-1f3a-466a-8ab5-316c60d1c1d5'}
        mock_post.return_value = mock_response

        # Define a sample request JSON
        request_json = {
            "calls": [["input_table", "output_table", "{}"]]
        }

        # Call the synthesize function
        from main import synthesize
        response = synthesize(Mock(get_json=lambda: request_json))

        # Check if the function returns the expected response
        expected_response = {
            "replies": [{"status": "success", "task_id": "649531ec-1f3a-466a-8ab5-316c60d1c1d5"}]
        }
        self.assertEqual(response, expected_response)

    @patch('main.requests.post')
    def test_synthesize_failure(self, mock_post):
        # Define a mock response for requests.post
        mock_response = Mock()
        mock_response.status_code = 400  # Simulate a failure status code
        mock_post.return_value = mock_response

        # Define a sample request JSON
        request_json = {
            "calls": [["input_table", "output_table", "{}"]]
        }

        # Call the synthesize function
        from main import synthesize
        response = synthesize(Mock(get_json=lambda: request_json))

        # Check if the function returns the expected error response
        expected_response = {
            "replies": [{"status": "error", "message": "Request failed with status code: 400"}]
        }
        self.assertEqual(response, expected_response)

    @patch('main.requests.post')
    def test_synthesize_request_exception(self, mock_post):
        # Simulate a request exception by raising an error in requests.post
        mock_post.side_effect = requests.exceptions.RequestException("Test error")

        # Define a sample request JSON
        request_json = {
            "calls": [["input_table", "output_table", "{}"]]
        }

        # Call the synthesize function
        from main import synthesize
        response = synthesize(Mock(get_json=lambda: request_json))

        # Check if the function returns the expected error response
        expected_response = {
            "replies": [{"status": "error", "message": "An error occurred: Test error"}]
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
