# Tim's Ticker Picker (Robo-Advisor Project)

Link to project: https://github.com/prof-rossetti/intro-to-python/blob/master/projects/robo-advisor/README.md

## Prerequisites
Start by cloning this repo and saving it down to your GitHub Desktop application or other remote git system.

To be able to use Tim's Ticker Picker, you will need to visit https://www.alphavantage.co/support/#api-key and obtain an API key.

Create a new file in this repo called .env and place inside the API key you obtained in the following format:

```
ALPHAVANTAGE_API_KEY = INSERT_KEY_HERE
```

### Environment Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n robo-advisor-env python=3.7 # (first time only)
conda activate robo-advisor-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file you cloned by typing:

```sh
pip install -r requirements.txt
```

From within the virtual environment, navigate to the repo in your file system and demonstrate your ability to run the Python script from the command-line:

```sh
python app/robo_advisor.py
```

## Further Exploration Challenges accomplished / cool things to note about Tim's Ticker Picker

I added some cool things that might be unique, and I'd love to point them out!

1. Replaced a 100-day recent high/low with 52-week high/lows (using weekly data to prevent slowdown)
2. Provided an option of data visualization over time: you can choose whether or not to get a graph, as well as how long you want that graph to illustrate (100-days, or between 1-5 years back in the past!)

## Tim's Ticker Picker should be ready!

Dive in and use Tim's Ticker Picker! Enjoy!

### Disclaimer

Tim's Ticker Picker does not assume liability when recommending stocks. While his complicated, proprietary algorithm of recommendations in cutting edge, please do not invest too much: Invest what you are willing to lose.