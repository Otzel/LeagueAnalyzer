import requests
from flatten_dict import flatten

def get_data():
    api_key = "api_key=RGAPI-df5f3b29-766b-43ad-a2fc-d6f7c1d28ff7"

    # get matchid of last 20 matches
    getMatchids = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/Y4jhr6e1vWvF6q6Num4oQEgCvVcBkm7hXobkLh9f3L5LM3l_i8YLzUX80MhAHV6feLdi-G13WcDivw/ids?start=0&count=50&"
    response = requests.get(getMatchids + api_key)

    if response.status_code != 200:
        print("Error fetching match IDs:", response.status_code)
        return

    matchids = response.json()

    # get match data
    matches_json = []
    matches_url = "https://europe.api.riotgames.com/lol/match/v5/matches/"

    for match in matchids:
        match_response = requests.get(matches_url + match + "?" + api_key)

        if match_response.status_code == 200:
            match_data = match_response.json()
            matches_json.append(match_data)
        else:
            print(f"Error fetching data for match {match}: {match_response.status_code}")

        #flat_dict = flatten(response.json(),reducer='dot')
    return matches_json