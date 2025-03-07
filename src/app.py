import streamlit as st
import pandas as pd
import os

from database import update_csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "match_summary.csv")

@st.cache_data(ttl=0)
def load_data():
    if not os.path.exists(CSV_FILE):
        print("⚠️ CSV file not found! Creating an empty DataFrame.")
        return pd.DataFrame(columns=["MatchID", "Date", "Time", "Game Duration", "Win/Loss",
                                     "Champion (Lah)", "Lane Opponent Champion", "CS/min (Lah)",
                                     "Kills", "Deaths", "Assists", "Comment about Lane Opponent", "Comment about Macro"])

    return pd.read_csv(CSV_FILE, delimiter=";", encoding="utf-8", skip_blank_lines=True)

df = load_data()

st.title("League of Legends Match Tracker")

st.write("## Please enter your PUUID and your API-Key")
game_name = st.text_area("Enter your Game Name")
tag_line = st.text_area("Enter your Tag Line")
api_key = st.text_area("Enter your API-Key")

if st.button("🔄 Refresh Data"):
    update_csv(game_name, tag_line, api_key)
    st.success("✅ Data refreshed! Reloading...")
    st.rerun()

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
    df.loc[df["MatchID"] == selected_match, "Comment about Lane Opponent"] = new_note_opp
    df.loc[df["MatchID"] == selected_match, "Comment about Macro"] = new_note_macro
    df.to_csv(CSV_FILE, sep=";", index=False)
    st.success("Note saved!")
    st.rerun()

