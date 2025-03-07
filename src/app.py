import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load or create CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
CSV_FILE = os.path.join(BASE_DIR, "match_summary.csv")

# Load data
@st.cache_data(ttl=0)  # Ensure it reloads fresh data
def load_data():
    # Check if file exists before trying to read
    if not os.path.exists(CSV_FILE):
        print("⚠️ CSV file not found! Creating an empty DataFrame.")
        return pd.DataFrame(columns=["MatchID", "Date", "Time", "Game Duration", "Win/Loss",
                                     "Champion (Lah)", "Lane Opponent Champion", "CS/min (Lah)",
                                     "Kills", "Deaths", "Assists", "Comment"])

    # If file exists, read it
    return pd.read_csv(CSV_FILE, delimiter=";", encoding="utf-8", skip_blank_lines=True)

df = load_data()

# Title
st.title("League of Legends Match Tracker")

# --- SEARCH FUNCTION ---
st.sidebar.header("Search Matches")
search_champ = st.sidebar.text_input("Champion (Lah)")
search_opponent = st.sidebar.text_input("Lane Opponent")
search_win = st.sidebar.selectbox("Win/Loss", ["All", "Win", "Loss"])

filtered_df = df.copy()

if search_champ:
    filtered_df = filtered_df[filtered_df["Champion (Lah)"].str.contains(search_champ, case=False, na=False)]
if search_opponent:
    filtered_df = filtered_df[filtered_df["Lane Opponent Champion"].str.contains(search_opponent, case=False, na=False)]
if search_win != "All":
    filtered_df = filtered_df[filtered_df["Win/Loss"] == search_win]

# Display Filtered Table
st.write("### Match History")
st.dataframe(filtered_df)

# --- STATISTICS & CHARTS ---
st.write("### Performance Trends")

# Calculate KDA over time
df["KDA"] = (df["Kills"] + df["Assists"]) / df["Deaths"].replace(0, 1)  # Avoid division by zero

fig, ax = plt.subplots()
ax.plot(df["Date"], df["KDA"], marker='o', label="KDA")
ax.plot(df["Date"], df["CS/min (Lah)"], marker='x', label="CS/min")
ax.set_xlabel("Date")
ax.set_ylabel("Value")
ax.set_title("KDA & CS/min Trends")
ax.legend()
plt.xticks(rotation=45)

st.pyplot(fig)

# --- ADD NEW NOTES ---
st.write("### Add Notes")
selected_match = st.selectbox("Select MatchID", df["MatchID"])
new_note = st.text_area("Enter your note")

if st.button("Save Note"):
    df.loc[df["MatchID"] == selected_match, "Comment"] = new_note
    df.to_csv(CSV_FILE, sep=";", index=False)
    st.success("Note saved!")
    st.rerun()  # Refresh UI after saving

