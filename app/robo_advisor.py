#app/robo_advisor.py

#modules
import json
import csv
import os
from datetime import datetime
import time
#packages
import requests
from dotenv import load_dotenv
import plotly
import plotly.graph_objs as go

load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default = "OOPS")

#adapted from prof-rossetti (intended for groceries exercise)
def to_usd(my_price):
    return f"${my_price:,.2f}"

#code adapted from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


############################################
#       INTRO INPUT (GETTING TICKER)
############################################


print("Hello! Welcome to Tim's Ticker Picker!")
print("---------------------------------------------------------")
print("Enter a valid stock ticker to recieve some valuable info!")
user_choice = input ("$")

if len(user_choice) >= 5 and hasNumbers(user_choice) == False:
    print("Whoops! Looks like your ticker was not valid.")
    print("Goodbye!")
    exit()

ticker = user_choice

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&apikey={API_KEY}"
response = requests.get(request_url)

error_message = "Error Message"

if error_message in response.text:
    print()
    print("Whoops! Looks like your ticker cannot be found on ALPHAVANTAGE,")
    print("the resource Tim's Ticker Picker uses to generate recommendations.")
    print()
    print("Try again!")
    exit()


##################################################
#                  SOME SETUP                    #
##################################################

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys())

latest_day = dates[0]

###########################
#   Getting latest close  #
###########################

latest_close = parsed_response["Time Series (Daily)"][f"{latest_day}"]["4. close"]



###########################
#    Getting recent high  #
###########################

high_prices = []

for i in dates:
    high_prices.append(parsed_response["Time Series (Daily)"][f"{str(i)}"]["2. high"])

recent_high = max(high_prices)


###########################
#    Getting recent low  #
###########################

low_prices = []

for i in dates:
    low_prices.append(parsed_response["Time Series (Daily)"][f"{str(i)}"]["3. low"])

recent_low = min(low_prices)


####################################################################################################################
# Proprietary, extremely complicated algorithm that should never be copied without accrediting Tim's Ticker Picker #
####################################################################################################################

recommendation = "Don't Buy"
explanation = "Tim's Ticker Picker doesn't believe that there is enough opportunity here!"

if float(latest_close) <= float(recent_low) * 1.1:
    recommendation = "Buy!"
    explanation = "This stock is within 10 percent of its 100-day recent low! Buy it when it's cheap!"
elif float(latest_close) <= float(recent_low) * 1.3:
    recommendation = "Buy!"
    explanation = "This stock is within 30 percent of its 100-day recent low... be careful, but we like it!"
elif float(latest_close) >= float(recent_high) * .85:
    recommendation = "Don't Buy!"
    explanation = "This stock is within 15 percent of a its 100-day recent high. Proceed with caution!"
elif float(latest_close) >= float(recent_high) * .95:
    recommendation = "Don't Buy!"
    explanation = "This stock is within 5 percent of a its 100-day recent high. Too expensive!"



######################################################
#     WRITING TO CSV
######################################################

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above

    for i in dates:
        writer.writerow({
            "timestamp": f"{i}",
            "open": to_usd(float(parsed_response["Time Series (Daily)"][i]["1. open"])),
            "high": to_usd(float(parsed_response["Time Series (Daily)"][i]["2. high"])),
            "low": to_usd(float(parsed_response["Time Series (Daily)"][i]["3. low"])),
            "close": to_usd(float(parsed_response["Time Series (Daily)"][i]["4. close"])),
            "volume": parsed_response["Time Series (Daily)"][i]["6. volume"]
        })



##########################
#   Begin Output         #
##########################

# printing time formatting from https://stackoverflow.com/questions/3961581/in-python-how-to-display-current-time-in-readable-format

print("-------------------------")
print(f"SELECTED SYMBOL: {ticker}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA")
print(f"REQUEST AT: {time.ctime()}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print(f"RECOMMENDATION: {recommendation}")
print(f"RECOMMENDATION REASON: {explanation}")
print("-------------------------")
print(f"WRITING DATA TO {csv_file_path}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


########################################
#   Optional Graphing prices over time #
########################################


print("Would you like a visualization of the stock price over the past 100 days?")
choice = input("Please type 'Y' or 'N' to indicate yes or no!")

if choice.upper() == "N":
    print("Ok! Have a great day!")
    print()
else:
    #generating vizi#

    line_data = []

    for i in dates:
        day_info = {"date": i, "stock_price_usd": float(parsed_response["Time Series (Daily)"][i]["4. close"])}
        line_data.append(day_info)

    date_list = [x["date"] for x in line_data]
    stock_price_list = [x["stock_price_usd"] for x in line_data]

    plotly.offline.plot({
        "data": [go.Scatter(x=date_list, y=stock_price_list)],
        "layout": go.Layout(title=f"Stock Prices for ${ticker.upper()} Over Time")
    }, auto_open=True)
    print("----------------")
    print("GENERATING LINE GRAPH...")