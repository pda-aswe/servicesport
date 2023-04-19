import unittest
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, date, time
from src import sport

@patch("requests.get")
def test_next_match(mock_requests):
    obj = sport.SportAPI()

    mock_response = mock_requests.return_value
    mock_response.json.return_value = {
        "matches": [
            {
                "homeTeam": {
                    "name": "Team 1"
                },
                "awayTeam": {
                    "name": "Team 2"
                },
                "utcDate": "2023-04-18T12:00:00Z",
                "status": "SCHEDULED",
                "season": {
                    "currentMatchday": 4
                }
            }
        ]
    }

    result = obj.get_next_match()

    assert result == (4, "Team 1", "Team 2", datetime(2023, 4, 18).date(), datetime(2023, 4, 18, 12, 0).time())
    mock_requests.assert_called_with("https://api.football-data.org/v2/competitions/BL1/matches", headers=obj.headers)


@patch("requests.get")
def test_current_matches(mock_requests):
    obj = sport.SportAPI()

    mock_response = mock_requests.return_value
    mock_response.json.return_value = {
        "matches": [{
            "homeTeam": {"name": "Team A"},
            "awayTeam": {"name": "Team B"},
            "score": {"fullTime": {"homeTeam": None, "awayTeam": None}}
        }]
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
