import os
import webbrowser
from backtesting import Backtest, Strategy
import pandas as pd
import warnings
from Utils import *
from settings import *

if os.name == "nt":  # Windows
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
elif os.name == "posix":  # macOS
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
else:
    raise EnvironmentError("Unsupported Operating System")

webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))

warnings.filterwarnings("ignore", module="backtesting._plotting")
warnings.filterwarnings("ignore", module="backtesting._stats")


def run_backtest(df_input, ticker="EUR_USD", filename="out/plot", plot=True):
    df = df_input.copy()
    df.columns = [col.capitalize() for col in df.columns]
    if "Date" in df.columns:
        df.index = pd.to_datetime(df["Date"])
    df = df[["Open", "High", "Low", "Close"]]

    class SignalStrategy(Strategy):
        def init(self):
            self.signal = df_input["signal"]

        def next(self):
            current_signal = self.signal[self.data.index[-1]]
            if current_signal == 0:
                if self.position:
                    self.position.close()
            elif current_signal > 0:
                if not self.position or self.position.is_short:
                    self.position.close()
                    self.buy(size=abs(current_signal))
                    # self.buy()
            elif current_signal < 0:
                if not self.position or self.position.is_long:
                    self.position.close()
                    self.sell(size=abs(current_signal))
                    # self.sell()

    bt = Backtest(
        df,
        SignalStrategy,
        cash=200000,
        commission=0.00014,
        exclusive_orders=spreads[ticker],
        margin=margins[ticker],
    )

    output = bt.run()
    if plot:
        bt.plot(filename=filename, open_browser=False, resample=False)
    if openChrome:
        path = os.path.abspath(filename)
        webbrowser.get(using="chrome").open_new_tab(f"file://{path}.html")
    return output
