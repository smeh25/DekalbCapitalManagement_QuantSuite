class Position:
    def __init__(self, ticker, shares):
        self.ticker = ticker
        self.shares = shares

    def market_value(self):
        raise NotImplementedError("Subclasses must implement this method.")
