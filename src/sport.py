import requests
import json
from datetime import datetime

class SportAPI:
    # Set API endpoint URLs
    base_url = 'https://api.football-data.org/v2'
    next_matchday_url = f'{base_url}/competitions/BL1/matches'
    current_matches_url = f'{base_url}/matches?competitions=BL1&status=LIVE'

    # Set request headers
    headers = {'X-Auth-Token': '54d8e09e3daa4c32bc653fcea02465d9'}

    # Function to get the next matchday and date/time of the next match
    def get_next_match(self):
        # Request the next matchday
        response = requests.get(self.next_matchday_url, headers=self.headers)
        matchday_data = response.json()

        # Get the date and time of the next match
        next_match_data = matchday_data['matches'][0]
        next_match_datetime = datetime.fromisoformat(next_match_data['utcDate'].replace('Z', '+00:00'))

        # Return the matchday and date/time of the next match
        return matchday_data['matches'][0]['season']['currentMatchday'], next_match_data['homeTeam']['name'], next_match_data['awayTeam']['name'], next_match_datetime.date(), next_match_datetime.time()

    # Function to get the current matches and their scores, or a message if there are no matches currently happening
    def get_current_matches(self):
        # Request the current matches
        response = requests.get(self.get_current_matches, headers=self.headers)
        current_matches_data = response.json()

        # If there are current matches happening, print their scores
        if len(current_matches_data['matches']) > 0:
            matches = []
            for match in current_matches_data['matches']:
                matches.append((match['homeTeam']['name'], match['awayTeam']['name'], match['score']['fullTime']['homeTeam'], match['score']['fullTime']['awayTeam']))
            return matches
        # If there are no current matches happening, return a message and the details of the next match
        else:
            next_match = self.get_next_match()
            message = f"Currently, there is no live match happening. The next match is {next_match[1]} vs {next_match[2]} on {next_match[3]} at {next_match[4]}."
            return message

# # Example usage:
# if __name__ == "__main__":
#     # Get the next matchday and date/time of the next match
#     matchday, home_team, away_team, match_date, match_time = get_next_match()

#     # Print the next matchday and date/time of the next match
#     print(f"Next matchday: {matchday}")
#     print(f"Next match: {home_team} vs {away_team} on {match_date} at {match_time}")

#     # Get the current matches and their scores, or a message if there are no matches currently happening
#     current_matches = get_current_matches()

#     # If there are current matches happening, print their scores
#     if isinstance(current_matches, list):
#         for match in current_matches:
#             print(f"{match[0]} vs {match[1]}: {match[2]} - {match[3]}")
#     # If there are no current matches happening, print the message
#     else:
#         print(current_matches)
