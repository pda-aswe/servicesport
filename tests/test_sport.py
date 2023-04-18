import unittest
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, date, time
from src import sport

@patch("requests.get")
def test_current_matches(mock_requests):
    obj = sport.SportAPI()

    mock_response = mock_requests.return_value
    mock_response.json.return_value = {
        "matches": [
            {
                "homeTeam": {"name": "Bayern Munich"},
                "awayTeam": {"name": "Borussia Dortmund"},
                "score": {"fullTime": {"homeTeam": 1, "awayTeam": 0}}
            }
        ]
    }

    obj.get_current_matches()

    assert mock_requests.call_count > 0
    assert any(call[1]['headers']['X-Auth-Token'] == obj.headers['X-Auth-Token'] and
               call[0][0] == 'https://api.football-data.org/v2/matches?competitions=BL1&status=LIVE' for call in mock_requests.call_args_list)


@patch("requests.get")
def test_current_matches(mock_requests):
    obj = sport.SportAPI()

    mock_response = mock_requests.return_value
    mock_response.json.return_value = {
        "matches": [
            {
                "id": 1,
                "utcDate": "2023-04-19T18:30:00Z",
                "status": "LIVE",
                "score": {
                    "winner": None,
                    "fullTime": {
                        "homeTeam": None,
                        "awayTeam": None
                    }
                },
                "homeTeam": {
                    "name": "Team A"
                },
                "awayTeam": {
                    "name": "Team B"
                },
                "competition": {
                    "name": "Bundesliga"
                }
            }
        ]
    }

    result = obj.get_current_matches()

    expected_result = "Live match: Team A vs Team B, score: None - None"
    assert result == expected_result
    mock_requests.assert_called_once_with("https://api.football-data.org/v2/matches?competitions=BL1&status=LIVE", headers=obj.headers)


@patch("requests.get")
def test_current_matches_no_matches(mock_requests):
    obj = sport.SportAPI()

    mock_response = mock_requests.return_value
    mock_response.json.return_value = {
        "matches": []
    }

    result = obj.get_current_matches()

    expected_result = f"Currently, there is no live match happening. The next match is {obj.get_next_match()[1]} vs {obj.get_next_match()[2]} on {obj.get_next_match()[3]} at {obj.get_next_match()[4]}."
    assert result == expected_result
    mock_requests.assert_called_once_with("https://api.football-data.org/v2/matches?competitions=BL1&status=LIVE", headers=obj.headers)