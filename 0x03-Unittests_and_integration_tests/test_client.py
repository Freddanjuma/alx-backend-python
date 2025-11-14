#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and calls get_json once with the correct URL.
        """
        # Mocked return value (it can be anything, we only verify structure)
        mock_get_json.return_value = {"payload": True}

        client = GithubOrgClient(org_name)
        result = client.org

        # Ensure get_json was called ONLY once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Ensure result matches what get_json returned
        self.assertEqual(result, {"payload": True})

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct value
        based on the mocked GithubOrgClient.org property.
        """
        # Mock payload returned by .org
        mock_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}

        # Patch GithubOrgClient.org to return the mocked payload
        with patch('client.GithubOrgClient.org', return_value=mock_payload):
            client = GithubOrgClient("test")
            result = client._public_repos_url

            # Verify the correct repos_url is returned
            self.assertEqual(result, mock_payload["repos_url"])
