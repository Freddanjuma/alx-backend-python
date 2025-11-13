#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map.
"""
import unittest
from utils import access_nested_map
from parameterized import parameterized
from typing import Mapping, Sequence, Any
# --- NEW IMPORTS FOR THIS TASK ---
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json
# --- END NEW IMPORTS ---
from parameterized import parameterized
# --- NEW TYPE IMPORT FOR THIS TASK ---
from typing import Mapping, Sequence, Any, Dict
# --- END NEW TYPE IMPORT ---


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for the access_nested_map function.
    """

    # --- Test 1 (Your first test) ---
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected: Any
    ) -> None:
        """
        Test that access_nested_map returns the correct value using
        parameterized inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    # --- Test 2 (The new test for this task) ---
    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected_key: str
    ) -> None:
        """
        Test that access_nested_map raises a KeyError for invalid paths
        and checks the exception message.

       """
       
class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for the access_nested_map function.
    (This is your existing class from the previous tasks)
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected: Any
    ) -> None:
        """
        Test that access_nested_map returns the correct value using
        parameterized inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b'),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected_key: str
    ) -> None:
        """
        Test that access_nested_map raises a KeyError for invalid paths
        and checks the exception message.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        self.assertEqual(str(cm.exception), f"'{expected_key}'")


# --- THIS IS THE EXACT TEST CODE FOR THE NEW TASK ---
class TestGetJson(unittest.TestCase):
    """
    Test class for the get_json function with mocking.
    """

    # 1. Use @parameterized.expand with the two inputs
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
        self,
        test_url: str,
        test_payload: Dict,
    ) -> None:
        """
        Test that get_json returns the expected payload by mocking
        the requests.get call.
        """
        # 2. Use unittest.mock.patch to patch 'utils.requests.get'
        #    We patch 'utils.requests.get' because that is the path
        #    used inside the `get_json` function.
        with patch('utils.requests.get') as mock_get:
            # 3. Create a Mock object to simulate the response
            mock_response = Mock()
            # 4. Set the mock response's .json() method to return test_payload
            mock_response.json.return_value = test_payload
            # 5. Set the mock 'requests.get' to return our mock response
            mock_get.return_value = mock_response

            # Call the function we are testing
            result = get_json(test_url)

            # 6. Test that the mocked get method was called exactly once
            #    with test_url as the argument.
            mock_get.assert_called_once_with(test_url)

            # 7. Test that the output of get_json is equal to test_payload
            self.assertEqual(result, test_payload)
# --- END OF THE NEW TEST CODE ---


# --- This part just makes the test file runnable ---
if __name__ == '__main__':
    unittest.main()

        # Use the assertRaises context manager to catch the KeyError
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # Check that the exception message is the key that caused the error
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


# --- This part just makes the test file runnable ---
# This MUST be at the very end of the file.
if __name__ == '__main__':
    unittest.main()