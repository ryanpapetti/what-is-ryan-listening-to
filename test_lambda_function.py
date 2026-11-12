import sys
import unittest
from types import ModuleType
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Keep this unit test runnable without installing the Lambda deployment package.
requests_stub = ModuleType('requests')
requests_stub.session = Mock()
sys.modules.setdefault('requests', requests_stub)

import lambda_function


class CurrentListeningTests(unittest.TestCase):
    def test_playing_returns_serialized_statement(self):
        response = Mock(status_code=200)
        response.json.return_value = {
            'item': {'name': 'A song', 'artists': [{'name': 'An artist'}]},
        }
        session = Mock()
        session.get.return_value = response

        with patch.object(lambda_function.requests, 'session', return_value=session):
            result = lambda_function.lambda_handler({'body': {}}, None)

        self.assertEqual(result['body'],
                         '{"statement": "Ryan is listening to A song by An artist"}')

    def test_not_listening_returns_proxy_response_with_real_header_values(self):
        response = Mock(status_code=204)
        session = Mock()
        session.get.return_value = response

        with patch.object(lambda_function.requests, 'session', return_value=session):
            result = lambda_function.lambda_handler({'body': {}}, None)

        self.assertEqual(result['headers'], {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
        })
        self.assertIs(result['isBase64Encoded'], False)
        self.assertEqual(
            result['body'],
            '{"statement": "Ryan is not listening to anything on Spotify right now."}',
        )


if __name__ == '__main__':
    unittest.main()
