#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map.
"""
import unittest
from utils import access_nested_map
from parameterized import parameterized
from typing import Mapping, Sequence, Any


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
        # Use the assertRaises context manager to catch the KeyError
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # Check that the exception message is the key that caused the error
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


# --- This part just makes the test file runnable ---
# This MUST be at the very end of the file.
if __name__ == '__main__':
    unittest.main()