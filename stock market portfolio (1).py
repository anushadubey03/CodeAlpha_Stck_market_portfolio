#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

class StockPortfolio:
    def __init__(self, api_key):
        self.api_key = api_key
        self.portfolio = {}

    def add_stock(self, symbol, quantity):
        if symbol in self.portfolio:
            self.portfolio[symbol] += quantity
        else:
            self.portfolio[symbol] = quantity

    def remove_stock(self, symbol, quantity):
        if symbol in self.portfolio:
            if quantity >= self.portfolio[symbol]:
                del self.portfolio[symbol]
            else:
                self.portfolio[symbol] -= quantity
        else:
            print("Stock not found in portfolio.")

    def get_portfolio_value(self):
        ts = TimeSeries(key=self.api_key, output_format='pandas')
        total_value = 0

        for symbol, quantity in self.portfolio.items():
            data, _ = ts.get_quote_endpoint(symbol)
            stock_price = float(data['05. price'][0]) 
            total_value += stock_price * quantity

        return total_value

    def plot_portfolio_performance(self):
        ts = TimeSeries(key=self.api_key, output_format='pandas')
        dates = None
        portfolio_value = None

        for symbol, quantity in self.portfolio.items():
            data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
            data = data['4. close'].iloc[::-1]
            if dates is None:
                dates = data.index.tolist()
            stock_value = data * quantity
            if portfolio_value is None:
                portfolio_value = stock_value
            else:
                portfolio_value += stock_value

        plt.plot(dates, portfolio_value)
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.title('Portfolio Performance')
        plt.xticks(rotation=45)
        plt.show()


api_key = 'U2F8KEF5Z84GV72B'
portfolio = StockPortfolio(api_key)

portfolio.add_stock('AAPL', 5)
portfolio.add_stock('GOOGL', 2)
portfolio.add_stock('MSFT', 3)

print("Portfolio Value:", portfolio.get_portfolio_value())
portfolio.plot_portfolio_performance()


# In[ ]:




