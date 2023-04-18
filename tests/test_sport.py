from src import sport
from unittest.mock import patch, ANY, mock_open

@patch("builtins.open")
@patch("os.path.exists")
@patch("requests.get")
def test_next_match(mock_requests, mock_exists, mock_open):
    obj = sport.SportAPI
    
    obj.get_next_match(self)
    mock_requests.assert_called_with(f"https://api.football-data.org/v2/competitions/BL1/matches")


@patch("builtins.open")
@patch("os.path.exists")
@patch("requests.get")
def test_current_matches(mock_requests, mock_exists, mock_open):
    obj = sport.SportAPI
    
    obj.get_current_matches(self)
    mock_requests.assert_called_with(f"https://api.football-data.org/v2/matches?competitions=BL1&status=LIVE")
