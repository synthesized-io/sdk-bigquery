import unittest
import requests
from unittest.mock import Mock, patch
import os


class TestCheckFunction(unittest.TestCase):

    def setUp(self):
        # Set up environment variable for testing
        os.environ['FLOWER_API_URL'] = 'http://test-flower.com'

    def tearDown(self):
        # Clean up environment variable after testing
        del os.environ['FLOWER_API_URL']

    @patch('main.requests.get')
    def test_check_success(self, mock_get):
        # Define a mock response for requests.post
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'task-id': "649531ec-1f3a-466a-8ab5-316c60d1c1d5", 'state': 'completed'}
        mock_get.return_value = mock_response

        # Define a sample request JSON
        request_json = {
            "calls": [["649531ec-1f3a-466a-8ab5-316c60d1c1d5"]]
        }

        # Call the synthesize function
        from main import get_task_status
        response = get_task_status(Mock(get_json=lambda: request_json))

        # Check if the function returns the expected response
        expected_response = {
            "replies": [{"status": "completed"}]
        }
        self.assertEqual(response, expected_response)

    @patch('main.requests.get')
    def test_check_not_found(self, mock_get):
        # Define a mock response for requests.post
        mock_response = Mock()
        mock_response.status_code = 404  # Simulate a not found status code
        mock_get.return_value = mock_response

        # Define a sample request JSON
        request_json = {
            "calls": [["649531ec-1f3a-466a-8ab5-316c60d1c1d5"]]
        }

        # Call the synthesize function
        from main import get_task_status
        response = get_task_status(Mock(get_json=lambda: request_json))

        # Check if the function returns the expected error response
        expected_response = {
            "replies": [{"status": "not found"}]
        }
        self.assertEqual(response, expected_response)

    @patch('main.requests.get')
    def test_check_request_exception(self, mock_get):
        # Simulate a request exception by raising an error in requests.post
        mock_get.side_effect = requests.exceptions.RequestException("Test error")

        # Define a sample request JSON
        request_json = {
            "calls": [["649531ec-1f3a-466a-8ab5-316c60d1c1d5"]]
        }

        # Call the synthesize function
        from main import get_task_status
        response = get_task_status(Mock(get_json=lambda: request_json))

        # Check if the function returns the expected error response
        expected_response = {
            "replies": [{"status": "Test error"}]
        }
        self.assertEqual(response, expected_response)


if __name__ == '__main__':
    unittest.main()
