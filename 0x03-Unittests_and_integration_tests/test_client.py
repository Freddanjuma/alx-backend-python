#!/usr/bin/env python3
"""
Unit tests for client.py
"""
import unittest
# We need to import 'patch', 'Mock', 'PropertyMock', and 'MagicMock'
from unittest.mock import patch, Mock, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
# We need to import the payloads for the integration test
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Test class for GithubOrgClient.
    (This contains tasks 5 and 6)
    """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """
        Test that GithubOrgClient.org returns the correct value
        and that get_json is called once with the correct URL.
        """
        test_payload = {"name": org_name, "description": "Test org"}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org()
        self.assertEqual(result, test_payload)

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self) -> None:
        """
        Test that _public_repos_url returns the correct URL from the org payload.
        """
        # Create a mock org payload
        known_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        # Use patch as a context manager to mock the 'org' property
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock,
            return_value=known_payload
        ) as mock_org:
            client = GithubOrgClient("google")
            result = client._public_repos_url

            # Assert the result is correct
            self.assertEqual(result, "https://api.github.com/orgs/google/repos")
            # Assert that the 'org' property was accessed once
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """
        Test that public_repos returns the correct list of repos.
        (This is the test that was failing in your screenshot)
        """
        # Define a sample payload for the mock get_json
        repos_payload = [
            {"name": "repo1", "license": "mit"},
            {"name": "repo2", "license": "apache"}
        ]
        mock_get_json.return_value = repos_payload

        # Mock the _public_repos_url property
        # --- FIX FOR E501 (Line 41) ---
        # The line was too long, so we break it here
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value="https.api.github.com/orgs/google/repos"
        ) as mock_public_repos_url:

            client = GithubOrgClient("google")
            result = client.public_repos()

            # Assert the result is the expected list of repo names
            self.assertEqual(result, ["repo1", "repo2"])

            # Assert the property was accessed once
            mock_public_repos_url.assert_called_once()
            # Assert get_json was called once with the correct URL
            # --- FIX FOR E501 (Line 58) ---
            # This line was also too long, so we break it
            mock_get_json.assert_called_once_with(
                "https.api.github.com/orgs/google/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": None}, "my_license", False),
        ({}, "my_license", False)
    ])
    def test_has_license(
        self,
        repo: dict,
        license_key: str,
        expected: bool
    ) -> None:
        """
        Test the has_license static method.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


# We add 2 blank lines here to fix Pycodestyle
@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class for GithubOrgClient using fixtures.
    (This is for Task 7)
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the class-level patcher for requests.get.
        """
        mock_get = MagicMock()

        def get_side_effect(url):
            if url == f"https://api.github.com/orgs/google":
                return MagicMock(json=lambda: cls.org_payload)
            if url == cls.org_payload["repos_url"]:
                return MagicMock(json=lambda: cls.repos_payload)
            return MagicMock()

        mock_get.side_effect = get_side_effect

        cls.get_patcher = patch('requests.get', new=mock_get)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Stop the class-level patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Integration test for the public_repos method.
        """
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Integration test for public_repos with a license filter.
        """
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


# This MUST be at the very end of the file
if __name__ == '__main__':
    unittest.main()
