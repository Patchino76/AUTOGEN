# filename: microsoft_stock.py
#%%
import yfinance as yf

# Get Microsoft stock data for the year 2024
msft = yf.Ticker("MSFT").history(period="1y", start="2024-01-01", end="2025-01-01")
#%%
# Filter the data to keep only the days when MSFT closing price was higher than $370
desired_days = [date for date, close in msft['Close'].items() if close> 370]

#%%
print("The following are the dates in 2024 when Microsoft Stock closed higher than $370:")
for date in desired_days:
    print(date)
# %%
