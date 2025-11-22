#!/usr/bin/env python3
"""
Unit tests for utils.py functions.
"""
import unittest
from unittest.mock import patch, Mock
# Make sure to import memoize!
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for the access_nested_map function.
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
        Test that access_nested_map returns the correct value.
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
        Test that access_nested_map raises KeyError for invalid paths.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        self.assertEqual(str(cm.exception), f"'{expected_key}'")


# Two blank lines are required before a new class
class TestGetJson(unittest.TestCase):
    """
    Test class for the get_json function with mocking.
    """

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
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


# Two blank lines are required before a new class
class TestMemoize(unittest.TestCase):
    """
    Test class for the memoize decorator.
    """

    def test_memoize(self) -> None:
        """
        Test that when a method decorated with @memoize is called
        multiple times, the underlying method is only called once.
        """
        class TestClass:
            """A test class to use the memoize decorator on."""
            def __init__(self):
                self.call_count = 0

            def a_method(self):
                """A method to be memoized."""
                self.call_count += 1
                return 42

            @memoize
            def a_property(self):
                """A property that uses the memoized method."""
                return self.a_method()

        # We patch 'a_method' to spy on it
        with patch.object(
            TestClass,
            'a_method',
            # The 'wraps' argument was causing the error, so we remove it.
            # wraps=TestClass.a_method
        ) as mock_method:
            # We replace 'wraps' with this line to provide a return value
            mock_method.return_value = 42

            test_obj = TestClass()

            # Call the memoized property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            # Check that the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Check that the underlying method was called only ONCE
            mock_method.assert_called_once()


# This MUST be at the very end of the file
if __name__ == '__main__':
    unittest.main
    