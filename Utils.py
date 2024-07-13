from datetime import time, timedelta
import pandas as pd
import pytz
from twilio.rest import Client


margins = {
    "USD_CAD": 2.0 / 100,
    "EUR_USD": 1,
    "GBP_CAD": 3.0 / 100,
    "EUR_CAD": 3.0 / 100,
    "AUD_CAD": 3.0 / 100,
    "GBP_USD": 4.5 / 100,
    "AUD_USD": 4.5 / 100,
}
spreads = {
    "USD_CAD": 1.8 * 0.0001,
    "EUR_USD": 1.5 * 0.0001,
    "GBP_CAD": 4.6 * 0.0001,
    "EUR_CAD": 3.4 * 0.0001,
    "AUD_CAD": 2.5 * 0.0001,
    "GBP_USD": 1.5 * 0.0001,
    "AUD_USD": 1.5 * 0.0001,
}

balance_risks = {
    "USD_CAD": 0.9,
    "EUR_USD": 0.9,
    "GBP_CAD": 0.9,
    "EUR_CAD": 0.9,
    "AUD_CAD": 0.9,
    "GBP_USD": 0.9,
    "AUD_USD": 0.9,
}


def readCsv(filename):
    if "oanda" in filename:
        df = pd.read_csv(filename)
    else:
        df = pd.read_csv(
            filename,
            sep="\t",
            usecols=["Time", "Open", "High", "Low", "Close", "Volume"],
            parse_dates=["Time"],
        )
    df.columns = df.columns.str.lower()
    df.index = pd.to_datetime(df["time"])
    df = df[["open", "high", "low", "close"]]
    return df
