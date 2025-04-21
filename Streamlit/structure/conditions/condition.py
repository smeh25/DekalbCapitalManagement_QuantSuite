# condition.py
import pandas as pd
from utils.indicators import compute_indicator  # assume a generic compute_indicator function

class Condition:
    def __init__(self, ticker, indicator, operator, value, period):
        self.ticker = ticker
        self.indicator = indicator
        self.operator = operator
        self.value = value
        self.period = period

        self.data = None       # The computed indicator values
        self.boolData = None   # The boolean Series after evaluation

        self._initialize()

    def _initialize(self):
        # Load historical data from ticker with the given period
        self.ticker = self.ticker.__class__(self.ticker.symbol, period=self.period)
        df = self.ticker.historical_prices.copy()

        # Compute indicator column (add to df)
        try:
            df[self.indicator] = compute_indicator(df, self.indicator)
            self.data = df[self.indicator]
            self.boolData = self._evaluate(df[self.indicator])

        except Exception as e:
            raise ValueError(f"Error initializing condition for {self.indicator}: {e}")

    def _evaluate(self, series):
        if self.operator == '<':
            return series < self.value
        elif self.operator == '>':
            return series > self.value
        elif self.operator == '<=':
            return series <= self.value
        elif self.operator == '>=':
            return series >= self.value
        elif self.operator == '==':
            return series == self.value
        elif self.operator == '!=':
            return series != self.value
        else:
            raise ValueError(f"Unsupported operator: {self.operator}")