from structure.positions.base import Position

class StockPosition(Position):
    def __init__(self, ticker, shares):
        super().__init__(ticker, shares)

    def market_value(self):
        return self.shares * self.ticker.current_price

    def __repr__(self):
        return f"<Stock: {self.ticker.symbol}, Shares: {self.shares}>"
