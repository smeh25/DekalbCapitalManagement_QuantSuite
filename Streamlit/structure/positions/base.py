class Position:
    def __init__(self, ticker, shares):
        self.ticker = ticker
        self.shares = shares
        self.isOption = False

    def market_value(self):
        raise NotImplementedError("Subclasses must implement this method.")
