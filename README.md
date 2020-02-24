# robo-advisor

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

If you see the example output, you're ready to move on to project development. This would be a great time to make any desired modifications to your project's "README.md" file (like adding instructions for how to setup and run the app like you've just done), and then make your first commit, with a message like "Setup the repo".