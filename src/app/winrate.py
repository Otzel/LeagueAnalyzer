import streamlit as st
import pandas as pd


def calculate_winrate(df, min_games):
    """Calculate winrate against different lane opponents with a minimum game filter."""
    if df.empty:
        return pd.DataFrame(columns=["Lane Opponent", "Games Played", "Wins", "Losses", "Winrate %"])

    winrate_df = df.groupby("Lane_Opponent").agg(
        Games_Played=("Win/Loss", "count"),
        Wins=("Win/Loss", lambda x: (x == "Win").sum()),
        Losses=("Win/Loss", lambda x: (x == "Loss").sum())
    ).reset_index()

    # Calculate winrate percentage
    winrate_df["Winrate %"] = (winrate_df["Wins"] / winrate_df["Games_Played"] * 100).round(2)

    # Filter out champions with fewer than `min_games` played
    winrate_df = winrate_df[winrate_df["Games_Played"] >= min_games]

    return winrate_df.sort_values(by="Winrate %", ascending=False)


def display_winrate(df):
    """Streamlit UI for displaying the winrate table with adjustable filtering."""
    st.write("## Winrate Against Lane Opponents")

    # User selects the minimum number of games to display
    min_games = st.slider("Minimum Games Against Opponent", min_value=1, max_value=20, value=5)

    winrate_df = calculate_winrate(df, min_games)

    if winrate_df.empty:
        st.warning(f"No opponents with at least {min_games} games played.")
    else:
        st.dataframe(winrate_df, use_container_width=True)
