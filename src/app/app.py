import streamlit as st
import pandas as pd
import os

from core.database import fetch_all_matches, update_notes_in_db
from core.dataHandler import update_database

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_FILE = os.path.join(DATA_DIR, "match_summary.csv")

os.makedirs(DATA_DIR, exist_ok=True)

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

st.write("## Please enter your PUUID and your API-Key")

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    game_name = st.text_input("Game Name", max_chars=64)

with col2:
    tag_line = st.text_input("Tag Line", max_chars=8)

with col3:
    api_key = st.text_input("API Key", type="password", max_chars=60)

st.markdown("<br>", unsafe_allow_html=True)
st.button("🔄 Refresh Data", use_container_width=True, on_click=lambda: [update_database(game_name, tag_line, api_key), st.rerun()])

st.sidebar.header("Search Matches")
search_champ = st.sidebar.text_input("Champion")
search_opponent = st.sidebar.text_input("Lane Opponent")
search_win = st.sidebar.selectbox("Win/Loss", ["All", "Win", "Loss"])

filtered_df = df.copy()

if search_champ:
    filtered_df = filtered_df[filtered_df["Champion (Lah)"].str.contains(search_champ, case=False, na=False)]
if search_opponent:
    filtered_df = filtered_df[filtered_df["Lane Opponent Champion"].str.contains(search_opponent, case=False, na=False)]
if search_win != "All":
    filtered_df = filtered_df[filtered_df["Win/Loss"] == search_win]

st.write("### Match History")
st.dataframe(filtered_df)

# # --- STATISTICS & CHARTS ---
# st.write("### Performance Trends")
#
# # Calculate KDA over time
# df["KDA"] = (df["Kills"] + df["Assists"]) / df["Deaths"].replace(0, 1)  # Avoid division by zero
#
# fig, ax = plt.subplots()
# ax.plot(df["Date"], df["KDA"], marker='o', label="KDA")
# ax.plot(df["Date"], df["CS/min (Lah)"], marker='x', label="CS/min")
# ax.set_xlabel("Date")
# ax.set_ylabel("Value")
# ax.set_title("KDA & CS/min Trends")
# ax.legend()
# plt.xticks(rotation=45)
#
# st.pyplot(fig)

st.write("### Add Notes")
selected_match = st.selectbox("Select MatchID", df["MatchID"])
new_note_opp = st.text_area("Enter your notes about you lane opponent")
new_note_macro = st.text_area("Enter your notes about you Macro")


if st.button("Save Notes"):
    update_notes_in_db(selected_match, new_note_opp, new_note_macro)
    st.success("✅ Notes saved to database!")
    st.rerun()

