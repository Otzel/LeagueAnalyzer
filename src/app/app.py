import streamlit as st
import pandas as pd
import os

from core.database import fetch_all_matches, update_notes_in_db
from core.dataHandler import update_database
from winrate import display_winrate  # Import the new tab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_FILE = os.path.join(DATA_DIR, "match_summary.csv")

os.makedirs(DATA_DIR, exist_ok=True)

default_columns = ["MatchID", "Date", "Time", "Champion", "Lane_Opponent", "Win/Loss", "CS_per_min", "Kills", "Deaths",
                   "Assists", "Comment_Lane", "Comment_Macro"]


@st.cache_data(ttl=0)
def load_data():
    matches = fetch_all_matches()

    columns = ["MatchID", "Date", "Time", "Duration", "Win", "Champion",
               "Lane_Opponent", "CS_per_min", "Kills", "Deaths", "Assists",
               "Comment_Lane", "Comment_Macro"]

    df = pd.DataFrame(matches, columns=columns)

    df["Win/Loss"] = df["Win"].map({1: "Win", 0: "Loss"})

    df.drop(columns=["Win"], inplace=True)

    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.time

    df = df.sort_values(by=["Date", "Time"], ascending=[False, False])

    return df


df = load_data()

st.title("League of Legends Match Tracker")

# --- TABS ---
tab1, tab2 = st.tabs(["📜 Match History", "📊 Winrate Analysis"])

with tab1:
    st.write("## Match History")

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        game_name = st.text_input("Game Name", max_chars=64)
    with col2:
        tag_line = st.text_input("Tag Line", max_chars=8)
    with col3:
        api_key = st.text_input("API Key", type="password", max_chars=60)

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("🔄 Refresh Data", use_container_width=True,
              on_click=lambda: [update_database(game_name, tag_line, api_key), st.rerun()])

    st.sidebar.header("Search Matches")
    search_champ = st.sidebar.text_input("Champion")
    search_opponent = st.sidebar.text_input("Lane Opponent")
    search_win = st.sidebar.selectbox("Win/Loss", ["All", "Win", "Loss"])

    filtered_df = df.copy()
    if search_champ:
        filtered_df = filtered_df[filtered_df["Champion"].str.contains(search_champ, case=False, na=False)]
    if search_opponent:
        filtered_df = filtered_df[filtered_df["Lane_Opponent"].str.contains(search_opponent, case=False, na=False)]
    if search_win != "All":
        filtered_df = filtered_df[filtered_df["Win/Loss"] == search_win]

    selected_columns = st.multiselect("Select columns to display", df.columns.tolist(), default=default_columns)

    st.write("### Match History")
    st.dataframe(filtered_df[selected_columns])

    st.write("### Add Notes")

    # Create a dictionary mapping MatchID to comments
    match_comments = {row["MatchID"]: (row["Comment_Lane"], row["Comment_Macro"]) for _, row in df.iterrows()}

    # Select MatchID
    selected_match = st.selectbox("Select MatchID", df["MatchID"])

    # Get existing comments (default to empty if no comment exists)
    existing_comment_lane, existing_comment_macro = match_comments.get(selected_match, ("", ""))

    # Pre-fill text boxes with existing comments
    new_note_opp = st.text_area("Enter your notes about your lane opponent", value=existing_comment_lane)
    new_note_macro = st.text_area("Enter your notes about your Macro", value=existing_comment_macro)

    if st.button("Save Notes"):
        update_notes_in_db(selected_match, new_note_opp, new_note_macro)
        st.success("✅ Notes saved to database!")
        st.rerun()

# Display Winrate Tab
with tab2:
    display_winrate(df)  # Call function from winrate.py
