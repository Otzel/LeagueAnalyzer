from riotAPI import get_data
from database import write_json, process_match_data

if __name__ == '__main__':
    # Fetch JSON data
    matches_json = get_data()
    #write_json(matches_json)
    process_match_data(matches_json)
