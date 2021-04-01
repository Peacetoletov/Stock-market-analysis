import yfinance as yf
import pandas

pandas.set_option('display.max_rows', None)
pandas.set_option('display.max_columns', None)

stock = yf.Ticker("amzn")

analytics = stock.recommendations
dataframe = analytics.filter(["Date", "To Grade", "From Grade", "Action"])
print(dataframe)
