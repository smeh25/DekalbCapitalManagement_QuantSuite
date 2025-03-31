from structure.positions.base import Position

class OptionPosition(Position):
    def __init__(self, ticker, shares, expiration, strike, option_type):
        super().__init__(ticker, shares)
        self.expiration = expiration
        self.strike = strike
        self.option_type = option_type

    def market_value(self):
        df = self.ticker.calls if self.option_type == "call" else self.ticker.puts
        if df is not None:
            row = df[df["strike"] == self.strike]
            if not row.empty:
                last_price = row["lastPrice"].iloc[0]
                return self.shares * 100 * last_price
        return 0.0

    def __repr__(self):
        return (f"<Option: {self.ticker.symbol} {self.option_type.upper()} "
                f"{self.strike} x {self.shares} @ {self.expiration}>")
