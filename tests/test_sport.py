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
        "matches": [{
            "homeTeam": {"name": "Team A"},
            "awayTeam": {"name": "Team B"},
            "score": {"fullTime": {"homeTeam": None, "awayTeam": None}}
        }]
    }

    result = obj.get_current_matches()

    expected_result = [('Team A', 'Team B', None, None)]
    assert result == expected_result

    mock_requests.assert_called_once_with(
        "https://api.football-data.org/v2/matches?competitions=BL1&status=LIVE",
        headers=obj.headers
    )


@patch("requests.get")
def test_current_matches_no_matches(mock_requests):
    obj = sport.SportAPI()

    mock_response = mock_requests.return_value
    mock_response.json.return_value = {
        "matches": []
    }

    result = obj.get_current_matches()

    next_match = obj.get_next_match()
    if next_match:
        expected_result = (
            f"Currently, there is no live match happening. "
            f"The next match is {next_match[1]} vs {next_match[2]} on {next_match[3]} at {next_match[4]}."
        )
    else:
        expected_result = "Currently, there is no live match happening. No matches are scheduled."

    assert result == expected_result

    mock_requests.assert_called_once_with(
        "https://api.football-data.org/v2/matches?competitions=BL1&status=LIVE",
        headers=obj.headers
    )
