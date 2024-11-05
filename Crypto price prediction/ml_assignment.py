
import requests
import pandas as pd
import datetime

API_KEY = 'b6703b7daaa226f49650b1be25f362c93dbee1e230111777283da115c0ff74dc'  
BASE_URL = "https://min-api.cryptocompare.com/data/v2/histoday"

# Parameters for request
params = {
    'fsym': 'BTC',       # Base cryptocurrency
    'tsym': 'USD',       # Quote currency
    'limit': 10,         # Number of days (10 days in this case)
    'api_key': API_KEY   # API Key
}

# Making the request
response = requests.get(BASE_URL, params=params)
data = response.json()

# Displaying the result
data

def fetch_crypto_data(crypto_pair, start_date, api_key):
    # Split the pair
    base_currency, quote_currency = crypto_pair.split("/")

    # Defining the API endpoint and parameters
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        'fsym': base_currency,
        'tsym': quote_currency,
        'toTs': int(datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp()),
        'limit': 365,   
        'api_key': api_key
    }

    # Sending the request
    response = requests.get(url, params=params)
    data = response.json()

    # Checking if the response is successful
    if data['Response'] == 'Success':
        # Extracting relevant data
        records = []
        for entry in data['Data']['Data']:
            records.append({
                "Date": datetime.datetime.fromtimestamp(entry['time']).strftime('%Y-%m-%d'),
                "Open": entry['open'],
                "High": entry['high'],
                "Low": entry['low'],
                "Close": entry['close']
            })

        # Converting to DataFrame
        df = pd.DataFrame(records)
        return df
    else:
        print("Error:", data['Message'])
        return None

crypto_pair = "BTC/USD"
start_date = "2023-01-01"
api_key = "b6703b7daaa226f49650b1be25f362c93dbee1e230111777283da115c0ff74dc"  # Replace with your actual CryptoCompare API key
df = fetch_crypto_data(crypto_pair, start_date, api_key)
df.head()

df.shape

def calculate_metrics(data, variable1, variable2):
    # Copying the data to avoid modifying the original DataFrame
    df = data.copy()

    
    df['Date'] = pd.to_datetime(df['Date'])

    # Calculating historical high and low metrics for look-back period (variable1)
    df[f'High_Last_{variable1}_Days'] = df['High'].rolling(window=variable1, min_periods=1).max()
    df[f'Low_Last_{variable1}_Days'] = df['Low'].rolling(window=variable1, min_periods=1).min()

    # Calculating days since last high and low for look-back period
    df[f'Days_Since_High_Last_{variable1}_Days'] = (df['Date'] - df['Date'].where(df['High'] == df[f'High_Last_{variable1}_Days']).ffill()).dt.days
    df[f'Days_Since_Low_Last_{variable1}_Days'] = (df['Date'] - df['Date'].where(df['Low'] == df[f'Low_Last_{variable1}_Days']).ffill()).dt.days

    # Calculating percentage difference from historical high and low for look-back period
    df[f'%_Diff_From_High_Last_{variable1}_Days'] = ((df['Close'] - df[f'High_Last_{variable1}_Days']) / df[f'High_Last_{variable1}_Days']) * 100
    df[f'%_Diff_From_Low_Last_{variable1}_Days'] = ((df['Close'] - df[f'Low_Last_{variable1}_Days']) / df[f'Low_Last_{variable1}_Days']) * 100

    # Calculating future high and low metrics for look-forward period (variable2)
    df[f'High_Next_{variable2}_Days'] = df['High'].shift(-variable2).rolling(window=variable2, min_periods=1).max()
    #The line below was changed to call the min function on the rolling window object.
    df[f'Low_Next_{variable2}_Days'] = df['Low'].shift(-variable2).rolling(window=variable2, min_periods=1).min()

    # Calculating percentage difference from future high and low for look-forward period
    df[f'%_Diff_From_High_Next_{variable2}_Days'] = ((df['Close'] - df[f'High_Next_{variable2}_Days']) / df[f'High_Next_{variable2}_Days']) * 100
    df[f'%_Diff_From_Low_Next_{variable2}_Days'] = ((df['Close'] - df[f'Low_Next_{variable2}_Days']) / df[f'Low_Next_{variable2}_Days']) * 100

    return df

variable1 = 7  
variable2 = 5  
metrics_df = calculate_metrics(df, variable1, variable2)
metrics_df.head()

metrics_df.to_csv("metri")

