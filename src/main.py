from database import update_csv
import pandas as pd

if __name__ == '__main__':
    #update_csv()
    # df = pd.read_csv("match_summary.csv", delimiter=";", encoding="utf-8")
    #
    # print(df.info())  # Check if rows exist
    # print(df.head())  # Show first few rows
    df = pd.read_csv("match_summary.csv", delimiter=";", encoding="utf-8", skip_blank_lines=True)
    print(df.info())  # Check if it loads rows now
    print(df.head())  # Print first few rows


