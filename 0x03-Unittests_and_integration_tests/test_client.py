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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos"""
        # Mock JSON payload returned by get_json
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        # Mock _public_repos_url to return a fixed URL
        with patch('client.GithubOrgClient._public_repos_url', 
                   return_value="https://api.github.com/orgs/test/repos") as mock_url:

            client = GithubOrgClient("test")
            repos = client.public_repos()

            # Test the expected list of repository names
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

            # Ensure the mocked URL property was accessed once
            mock_url.assert_called_once()

            # Ensure get_json was called once with that URL
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license with parameterized inputs."""
        client = GithubOrgClient("test")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get to return fixture payloads"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Configure side_effect to return different fixtures based on URL
        def side_effect(url, *args, **kwargs):
            mock_resp = Mock()
            if url.endswith("/orgs/google"):
                mock_resp.json.return_value = cls.org_payload
            elif url.endswith("/orgs/google/repos"):
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = {}
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the expected repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test that public_repos correctly filters by license"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
