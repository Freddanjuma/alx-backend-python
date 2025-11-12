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

    # We use the decorator to provide the test cases
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
        # This is the single line of test logic
        self.assertEqual(access_nested_map(nested_map, path), expected)


# This part just makes the test file runnable
if __name__ == '__main__':
    unittest.main()