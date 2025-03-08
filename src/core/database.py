import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_FILE = os.path.join(DATA_DIR, "matches.db")

os.makedirs(DATA_DIR, exist_ok=True)

def initialize_database():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS match_summary (
                MatchID TEXT PRIMARY KEY,
                Date TEXT CHECK(length(Date) = 10),  
                Time TEXT CHECK(length(Time) BETWEEN 4 AND 8),
                Duration TEXT, 
                Win INTEGER CHECK(Win IN (0, 1)), 
                Champion TEXT,
                Lane_Opponent TEXT,
                CS_per_min REAL,
                Kills INTEGER,
                Deaths INTEGER,
                Assists INTEGER,
                Comment_Lane TEXT,
                Comment_Macro TEXT
            )
        ''')
        conn.commit()

def insert_match(data):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO match_summary (MatchID, Date, Time, Duration, Win, Champion, Lane_Opponent, CS_per_min, Kills, Deaths, Assists)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['match_id'], data['Date'], data['Time'], data['Duration'], data['Win'], data['Champion'], data['Lane_Opponent'], data['CS/min'], data['Kills'], data['Deaths'], data['Assists'],))
        conn.commit()

def fetch_all_matches():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM match_summary")
        return cursor.fetchall()

def fetch_match_ids():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT MatchID FROM match_summary
        ''')
        conn.commit()
        return cursor.fetchall()

def fetch_match_by_id(match_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM match_summary WHERE MatchID = ?", (match_id,))
        return cursor.fetchone()
