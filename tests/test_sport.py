from src import sport
from unittest.mock import patch, ANY, mock_open

@patch("requests.get")
def test_next_match(mock_requests):
    obj = sport.SportAPI()
    
    obj.get_next_match()
    mock_requests.assert_called_with(f"https://api.football-data.org/v2/competitions/BL1/matches")

@patch("requests.get")
def test_current_matches(mock_requests):
    obj = sport.SportAPI()
    
    obj.get_current_matches()
    mock_requests.assert_called_with(f"https://api.football-data.org/v2/matches?competitions=BL1&status=LIVE")
