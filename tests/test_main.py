from src import main
from unittest.mock import patch, ANY, MagicMock
import json

@patch("sport.SportAPI")
def test_onMQTTconnect(mock_sport):

    mock_client = MagicMock()

    main.on_connect(mock_client,None,None,None)

    mock_client.subscribe.assert_called_with([('req/sport/next',0),('req/sport/now',0)])
    
    
@patch("sport.SportAPI")
def test_on_message(mock_sport):

    main.on_message(MagicMock(),None,message_for_testing())
    assert True

class message_for_testing:
    topic = "topic"
    payload = "payload"

@patch("sport.SportAPI")
def test_specific_callback_match_next(mock_sport):
    
    mock_client = MagicMock()
    msg = message_for_testing()
    msg.topic = "req/sport/next"
    msg.payload = MagicMock()
    
    main.sport_api = MagicMock()

    main.specific_callback(mock_client, None, msg)
    main.sport_api.get_next_match()

@patch("sport.SportAPI")
def test_specific_callback_matches_current(mock_sport):
    
    mock_client = MagicMock()
    msg = message_for_testing()
    msg.topic = "req/sport/now"
    msg.payload = MagicMock()
    
    main.sport_api = MagicMock()

    main.specific_callback(mock_client, None, msg)
    main.sport_api.sport_api.get_current_matches()