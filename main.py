import pandas as pd 
import yfinance as yf
from datetime import datetime
from tabulate import tabulate

# === QUARTER HELPER ===
def get_quarter(today=None):
    if today is None:
        today = datetime.today()
    year = today.year
    quarter = (today.month - 1) // 3 + 1
    if quarter == 1:
        start = f"{year}-01-01"
    elif quarter == 2:
        start = f"{year}-04-01"
    elif quarter == 3:
        start = f"{year}-07-01"
    elif quarter == 4:
        start = f"{year}-10-01"
    else:
        raise ValueError("Invalid quarter computed.")
    end = today.strftime("%Y-%m-%d")
    return start, end

# === OIL PRICE CHANGE ===
def get_oil_prices(ticker_symbol="CL=F"):
    ticker = yf.Ticker(ticker_symbol)
    start, end = get_quarter()
    data = ticker.history(start=start, end=end, interval="1mo")
    return data

def change_over_quarter(ticker_symbol="CL=F"):
    data = get_oil_prices(ticker_symbol)
    if data.empty or len(data) < 2:
        return None, None, None
    start_price = data["Close"].iloc[0]
    end_price = data["Close"].iloc[-1]
    change = ((end_price - start_price) / start_price) * 100
    return round(start_price, 2), round(end_price, 2), round(change, 2)

# === DELAY SCORING MODULE ===
def score_airlines_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    grouped_df = df.groupby("carrier_name").agg({
        "arr_flights": "sum",
        "arr_del15": "sum"
    }).reset_index()
    grouped_df["delay_rate"] = grouped_df["arr_del15"] / grouped_df["arr_flights"]
    grouped_df["delay_score"] = 100 * (1 - (grouped_df["delay_rate"] - grouped_df["delay_rate"].min()) /
                                            (grouped_df["delay_rate"].max() - grouped_df["delay_rate"].min()))
    _, _, oil_change = change_over_quarter("CL=F")

    def adjust_for_oil(score, oil_change):
        if oil_change is None:
            return score
        elif oil_change > 5:
            return score - 10
        elif oil_change < -5:
            return score + 10
        return score

    grouped_df["final_score"] = grouped_df["delay_score"].apply(lambda x: adjust_for_oil(x, oil_change))

    def recommend(score):
        if score >= 70:
            return "BUY"
        elif score >= 40:
            return "HOLD"
        else:
            return "SELL"

    grouped_df["recommendation"] = grouped_df["final_score"].apply(recommend)
    return grouped_df.sort_values(by="final_score", ascending=False)

# === DISPLAY TABLE ===
def display_table(df):
    table = df[["carrier_name", "final_score", "recommendation"]]
    print("\n--- Airline Equity Recommendations ---")
    print(tabulate(table, headers="keys", tablefmt="fancy_grid", showindex=False))

# === RUN ===
final_scores = score_airlines_from_csv("Airline_Delay_Cause.csv")
display_table(final_scores)

input("\nPress Enter to exit...")
