from .positions import StockPosition, OptionPosition
from .tickers import Ticker
import pandas as pd
import os

class Portfolio:
    def __init__(self):
        self.positions = []
        self.tickers = []
        self._load_from_csv()

    def _load_from_csv(self):
        filepath = os.path.join("raw_data", "uploadedInformation.csv")

        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            raise RuntimeError(f"Failed to read portfolio CSV: {e}")

        for _, row in df.iterrows():
            try:
                switch = False
                for i in self.tickers: 
                    if (i.symbol == row['Ticker'].upper()):
                        ticker = i
                        switch == True
                
                if (not switch):
                    ticker = Ticker(row["Ticker"])
                    self.tickers.append(ticker)

                type_ = row["Type"].lower()

                if type_ == "stock":
                    position = StockPosition(ticker, row["Shares"])
                elif type_ == "option":
                    position = OptionPosition(
                        ticker,
                        row["Shares"],
                        row["Expiration"],
                        row["Strike"],
                        row["OptionType"].lower()
                    )
                else:
                    continue  # Unknown type, skip

                self.add_position(position)
                ticker.add_position(position)

            except Exception as e:
                print(f"[Portfolio] Skipping row due to error: {e}")

    def add_position(self, position):
        self.positions.append(position)

    def total_value(self):
        return sum([p.current_price for p in self.positions])

    def __repr__(self):
        return f"<Portfolio with {len(self.positions)} positions | Value: ${self.total_value():,.2f}>"
