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


def to_usd(my_price):
    """
    This function was adapted from prof-rossetti (intended for groceries exercise).

    Parameter:
    arg1 (float): floating point to be converted to USD

    Returns:
    string: formatted my_price to USD
    """
    return f"${my_price:,.2f}"

def hasNumbers(inputString):
    """
    This function was adapted from https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number

    Parameter:
    arg1 (string): input to be tested if it contains a number in the string

    Returns:
    boolean: evaluated to true if no numbers in inputString
    """
    return any(char.isdigit() for char in inputString)

def couldNotBeFound(r):
    """
    This function will determine whether or not the parsed response contained an error message

    Parameter:
    arg1: response.text from the website

    Returns:
    boolean: evalutes to true if it does contain the error message
    """
    error_message = "Error Message"
    return error_message in r

def isInvalidTicker(t):
    """
    This function will determine whether or not the ticker is valid based on preliminary tests

    Parameter:
    arg1 (string): input ticker by the user

    Returns:
    boolean: evaluates to true if the length is greater or equal to 5 or has numbers in it
    """
    return len(t) >= 5 or hasNumbers(t) == True

def fetchDailyTicker(t):
    """
    This function grabs the DAILY data from alphavantage

    Parameter:
    arg1 (string): the user entered ticker

    Returns:
    the request from the website
    """
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={t}&apikey={API_KEY}"
    return requests.get(request_url)

def fetchWeeklyTicker(t):
    """
    This function grabs the WEEKLY data from alphavantage

    Parameter:
    arg1 (string): the user entered ticker

    Returns:
    the request from the website
    """
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={t}&apikey={API_KEY}"
    return requests.get(request_url)

def getLatestClose(pr):
    """
    This function grabs the latest close price

    Parameter:
    arg1 (dict): the parsed json response from the website

    Returns:
    float: the latest close price
    """
    return pr["Time Series (Daily)"][f"{latest_day}"]["4. close"]

def getRecentHigh():
    """
    This function grabs the most recent high over the last 52 weeks

    Returns:
    float: the 52 week high
    """
    high_prices = []
    count = 0

    for i in datesw:
        high_prices.append(parsed_weekly["Weekly Adjusted Time Series"][f"{str(i)}"]["2. high"])
        count = count + 1
        if count == 53:
            break

    return max(high_prices)

def getRecentLow():
    """
    This function grabs the most recent low over the last 52 weeks

    Returns:
    float: the 52 week low
    """
    low_prices = []
    count = 0

    for i in datesw:
        low_prices.append(parsed_weekly["Weekly Adjusted Time Series"][f"{str(i)}"]["3. low"])
        count = count + 1
        if count == 53:
            break

    return min(low_prices)

def adviseClient(close, low, high):
    """
    This function uses a proprietary algorithm to advise the client what to do about the stock they picked.

    Parameters:
    close (float): the recent close
    low (float): the 52 week low
    hgih (float): the 52 week high

    """

    recommendation = "Don't Buy"
    explanation = "Tim's Ticker Picker doesn't believe that there is enough opportunity here!"

    if float(latest_close) <= float(recent_low) * 1.1:
        recommendation = "Buy!"
        explanation = "This stock is within 10 percent of its 52-week recent low! Buy it when it's cheap!"
    elif float(latest_close) <= float(recent_low) * 1.3:
        recommendation = "Buy!"
        explanation = "This stock is within 30 percent of its 52-week recent low... be careful, but we like it!"
    elif float(latest_close) >= float(recent_high) * .85:
        recommendation = "Don't Buy!"
        explanation = "This stock is within 15 percent of a its 52-week recent high. Proceed with caution!"
    elif float(latest_close) >= float(recent_high) * .95:
        recommendation = "Don't Buy!"
        explanation = "This stock is within 5 percent of a its 52-week recent high. Too expensive!"

def dataToCSV():
    """
    This function writes the collected data to a csv file

    Returns:
    string: the csv file path the program wrote to
    """
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
    return csv_file_path

def outputFetchedData():
    """
    This function outputs the standard data collected
    """
    # printing time formatting from https://stackoverflow.com/questions/3961581/in-python-how-to-display-current-time-in-readable-format
    print("-------------------------")
    print(f"SELECTED SYMBOL: {ticker}")
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA")
    print(f"REQUEST AT: {time.ctime()}")
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"52-WEEK HIGH: {to_usd(float(recent_high))}")
    print(f"52-WEEK LOW: {to_usd(float(recent_low))}")
    print("-------------------------")
    print(f"RECOMMENDATION: {recommendation}")
    print(f"RECOMMENDATION REASON: {explanation}")
    print("-------------------------")
    print(f"WRITING DATA TO {csv_file_path}")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

if __name__ == "__main__":

    #################################################
    #       INTRO INPUT (GETTING TICKER DATA)       #
    #################################################


    print("Hello! Welcome to Tim's Ticker Picker!")
    print("---------------------------------------------------------")
    print("Enter a valid stock ticker to recieve some valuable info!")
    user_choice = input ("$")

    if isInvalidTicker(user_choice):
        print("Whoops! Looks like your ticker was not valid.")
        print("Goodbye!")
        exit()

    ticker = user_choice
    response = fetchDailyTicker(ticker)

    if couldNotBeFound(response.text):
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

    response = fetchWeeklyTicker(ticker)
    parsed_weekly = json.loads(response.text)

    tsdw = parsed_weekly["Weekly Adjusted Time Series"]
    datesw = list(tsdw.keys())

    ###########################
    #   Getting latest close  #
    ###########################

    latest_close = getLatestClose(parsed_response)

    ###########################
    #    Getting recent high  #
    ###########################

    recent_high = getRecentHigh()

    ###########################
    #    Getting recent low  #
    ###########################

    recent_low = getRecentLow()

    ####################################################################################################################
    # Proprietary, extremely complicated algorithm that should never be copied without accrediting Tim's Ticker Picker #
    ####################################################################################################################

    explanation = ""
    recommendation = ""

    adviseClient(latest_close, recent_low, recent_high)

    ###########################
    #     WRITING TO CSV      #
    ###########################

    csv_file_path = dataToCSV()

    ##########################
    #   Begin Output         #
    ##########################

    outputFetchedData()

    ########################################
    #   Optional Graphing prices over time #
    ########################################


    print("Would you like a visualization of the stock price over time?")
    print("Please type 'Y' or 'N' to indicate yes or no:")
    choice = input("-->")

    if choice.upper() == "N":
        print("Ok! Have a great day!")
        print()
        exit()

    print("Would you like it displayed over the past 100-days?")
    print("Or would you like it over the past several years?")
    print("Please indicate 'D' for the past 100-days or an integer between 1 and 5")
    print("to indicate how many years of data you would like to see.")
    choice = input("-->")

    valid_year_inputs = [1,2,3,4,5]

    if choice.upper() == "D":
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
    elif hasNumbers(choice) and int(choice) in valid_year_inputs:
        #generating vizi#

        line_data = []
        count = 0

        for i in datesw:
            week_info = {"week": i, "stock_price_usd": float(parsed_weekly["Weekly Adjusted Time Series"][i]["4. close"])}
            line_data.append(week_info)

            count = count + 1
            if count == (int(choice)*52) + 1:
                break


        week_list = [x["week"] for x in line_data]
        stock_price_list = [x["stock_price_usd"] for x in line_data]

        plotly.offline.plot({
            "data": [go.Scatter(x=week_list, y=stock_price_list)],
            "layout": go.Layout(title=f"Stock Prices for ${ticker.upper()} Over {choice} year(s)")
        }, auto_open=True)
        print("----------------")
        print("GENERATING LINE GRAPH...")
    else:
        print()
        print("It seems like you entered something other than 'D' or")
        print("a valid integer between 1 and 5.")
        print("-------------------------------------------------")
        print("Unfortunately, we cannot povide the graph to you!")
        print("-------------------------------------------------")
        print("Please try again!")
        print()