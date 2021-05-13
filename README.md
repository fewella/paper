# paper

This is the home for Trading Tommy! Tommy is a very simple trading bot that find opporunities to trade equity securities (stocks) on the NYSE. Currently, Tommy only makes decisions based on the price and the Relative Strength Index (RSI) of a symbol.


## How to use

### Step 1. Install required Python modules

To install all required Python modules as specified in `requirements.txt`, run: 

```
python -m pip install -r requirements.txt
```

### Step 2. Create a brokerage account with Alpaca

Follow the instruction on the [Alpaca](https://alpaca.markets/) website to create an account. 

### Step 3. Set the environment variables

For the bot to retrieve data from the Alpaca API, you must set the `APCA_API_KEY_ID` and `APCA_API_SECRET_KEY` environment variables to the API Key and API Secret Key listed in the account you create from step 2. 

*Note: We highly recommend you use a paper account (that simulates trades instead of placing real orders) while you get started!*

### Step 4. Run the bot

Navigate inside `python/` and run: 

```
python3 main.py
```

In addition, you can pass in the following arguments: 

* Run the custom function and exit - for testing purpose

```
-c, --custom
```

* Log debug messages

```
-d, --debug
```

* Suppresses all output except critical, overrides debug

```
-q, --quiet
```

* Store all output in the specified file

```
-o, --output
```

* Specify the timeframe over which to calculate signals and make trades, in MINUTES - [1, 1440]

```
-t, --timeframe
```

## How it works
