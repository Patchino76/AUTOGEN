#%%
import datetime
print("Today's date:", datetime.datetime.now().strftime("%Y-%m-%d"))
# %%
import requests
from bs4 import BeautifulSoup

def get_ytd_gain(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    ytd_gain = soup.find('span', {'data-test': 'common-stock-ytd'}).text.strip()
    return float(ytd_gain[1:]) # remove '%' sign
# %%
ticker1 = "META"
ticker2 = "TSLA"
ytd_gain1 = get_ytd_gain(ticker1)
# %%
