from __future__ import annotations

import unittest
from unittest.mock import patch, mock_open

from pre_commit_hooks.detect_gcp_credentials import detect_gcp_credentials_in_file, main


class TestDetect(unittest.TestCase):

    @patch('builtins.open', mock_open(read_data="Some content with GCP credentials: 'AIzaSyCzQ2rBq4dd8uf4Gh9J7G1IiCvC5q8oCvk'"))
    def test_detect_gcp_api_key(self):
        result = detect_gcp_credentials_in_file('')
        self.assertIn("AIzaSyCzQ2rBq4dd8uf4Gh9J7G1IiCvC5q8oCvk", result)

    @patch('builtins.open', mock_open(read_data="Some content with GCP credentials: '-----BEGIN PRIVATE KEY-----\nAbCdEf1234567890\n-----END PRIVATE KEY-----'"))
    def test_detect_gcp_service_account_key(self):
        result = detect_gcp_credentials_in_file('')
        self.assertIn("-----BEGIN PRIVATE KEY-----\nAbCdEf1234567890\n-----END PRIVATE KEY-----", result)

class TestMainFunction(unittest.TestCase):
    @patch('builtins.print')
    @patch('sys.stdin.read', return_value='/path/to/your/file.txt\n')  # Mocking stdin input
    @patch('pre_commit_hooks.detect_gcp_credentials.detect_gcp_credentials_in_file', return_value=['credential1', 'credential2'])
    def test_main_with_credentials(self, mock_detect, mock_input, mock_print):
        result = main()

        # Check if the output is as expected
        self.assertEqual(result, 1)  # Expecting a non-zero exit code
        mock_print.assert_any_call("🔴 Potential GCP credentials found:")
        mock_print.assert_any_call("credential1")
        mock_print.assert_any_call("credential2")
        mock_print.assert_any_call("Please remove these credentials before committing.")

    @patch('builtins.print')
    @patch('sys.stdin.read', return_value='/path/to/your/otherfile.txt\n')  # Mocking stdin input
    @patch('pre_commit_hooks.detect_gcp_credentials.detect_gcp_credentials_in_file', return_value=[])
    def test_main_without_credentials(self, mock_detect, mock_input, mock_print):
        result = main()

        # Check if the output is as expected
        self.assertEqual(result, 0)  # Expecting a zero exit code
        mock_print.assert_not_called()  # No potential credentials found, so print should not be called


if __name__ == '__main__':
    unittest.main()