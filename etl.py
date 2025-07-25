import requests, os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

load_dotenv()
#api key from coingecko.com
API_KEY = os.getenv("API_KEY").strip()

url = "https://api.coingecko.com/api/v3/simple/price"
#parameters like coins,currency
params = {
    "ids": "bitcoin,ethereum,solana",
    "vs_currencies": "usd",
    "include_market_cap": "true",
    "include_24hr_change": "true"
}
#file path to save data in .cvs format
save_path = "data/crypto_prices.csv"
#function to extract the data from coingecko.com
def extract_data():
    #pass your api key to headers
    headers = {"x_cg_pro_api_key": API_KEY}
    try:
        #get the data
        response = requests.get(url, params=params, headers=headers)
        #raise HTTPError for bad status codes
        response.raise_for_status()
        #store the in .json format
        data = response.json()
        #check if data has the expected structure
        if not data or not isinstance(data, dict):
            print("Unexpected API response format.")
            return None
        return data
    #handle errors
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occured: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occured: {req_err}")
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")
    return None
#function to transform data
def transform_data(data):
    #empty list
    rows = []
    #get the time when the program runs
    now = datetime.now().isoformat()
    #for every coin get the values
    for coin, values in data.items():
        #save each coin's parameters in a dictionary
        row = {
            "timestamp": now,
            "coin": coin,
            "price_usd": values["usd"],
            "market_cap": values["usd_market_cap"],
            "change_24h": values["usd_24h_change"]
        }
        #append the list with the dictionary created
        rows.append(row)
    #return a pandas datafram of the rows list
    return pd.DataFrame(rows)
#function to load data
def load_data(df):
    try:
        #try to find the old dataframe
        old_df = pd.read_csv(save_path)
        #the concatenate the old and new frames
        df = pd.concat([old_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    #create the folder data if it doesnt exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    #load the dataframe to a csv file
    df.to_csv(save_path, index=False)
    print(f"Saved to {save_path}")

def plot_prices(df, coin_name):
    #read the csv file for previously added entries
    try:
        df = pd.read_csv(save_path)
    except FileNotFoundError:
        print("No file found")
        return
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    #get a copy of every coin with bitcoin attribute
    coin_data = df[df["coin"] == coin_name].copy()
    if coin_data.empty:
        print(f"No data found for {coin_name}")
        return
    #gets the date today sets the hour to 00:00 and then sets the date to the first of the month
    start_date = pd.Timestamp.now().normalize().replace(day=1)
    #starts with the first day of the month and move to the last day of the same month
    end_date = (start_date + pd.offsets.MonthEnd(1))
    #gets every coin_name data with the timestamp of the current month
    filtered_data = coin_data[(coin_data["timestamp"]>= start_date) & (coin_data["timestamp"] <= end_date)]
    #create a figure for the plot 10inches wide and 5inches tall
    plt.figure(figsize=(10,5))
    #draw the graph with timestamp on x-axis and price_usd on y-axis marked with "o" at each point and connected with "-" 
    plt.plot(filtered_data["timestamp"], filtered_data["price_usd"], marker="o", linestyle="-")
    #set the title of the plot
    plt.title("Crypto Price Over Time (This Month)")
    #set the label for x-axis
    plt.xlabel("Time")
    #set the label for y-axis
    plt.ylabel("Price (USD)")
    #gca = get current axes so ax holds the axes of the plot
    ax = plt.gca()
    #set the spacing in x-axis and create a tick every ("interval=30") 30 mins
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    #sets the format for every tick in Hours:Mins ("%H:%M")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    #rotate the labels(ticks) on x-axis 45 degrees to make it easier to read and not overlap with each other
    plt.xticks(rotation=45)
    #adjust spacing of every element in the plot so they dont overlap
    plt.tight_layout()
    #display the plot window
    plt.show()


if __name__ == "__main__":
    #get the json formated data
    raw_data = extract_data()
    #check if raw_data is None
    if raw_data is None:
        print ("Failed to fetch data")
    else:
        #transforms the json data to dataframe
        df = transform_data(raw_data)
        #appends the new dataframe to existing data (if any) and saves or updates the csv file
        load_data(df)
        #check if the user wants a chart
        show_plot = input("Do you want to display the price chart? (y/n): ").strip().lower()
        #if he does
        if show_plot == "y":
            #allowed coin names
            allowed_coins = ["bitcoin", "ethereum", "solana"]
            while True:
                #user input coin name
                coin = input(f"Enter a coin name {','.join(allowed_coins)}:").strip().lower()
                #if its in allowed coin names
                if coin in allowed_coins:
                    break
                #if its not make the user re enter the name
                else:
                    print("Invalid coin name try again")
            #display the plot window of df
            plot_prices(df, coin)
       