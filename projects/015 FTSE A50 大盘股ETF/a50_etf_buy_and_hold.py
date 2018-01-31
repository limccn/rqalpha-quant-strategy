from rqalpha.api import *
import pandas as pd

data=pd.read_csv("./2823_holdings.csv",header=1,usecols=[0,2,3])
data.columns=["Ticker","Exchange","Weight"]
stocks_list = [str(data.iloc[i]["Ticker"]).zfill(6)+"."+data.iloc[i]["Exchange"] for i in range(len(data))]
stocks_share = [0.01*data.iloc[i]["Weight"] for i in range(len(data))]

def init(context):
    logger.info("init")
    context.s1 = stocks_list
    update_universe(context.s1)
    # initial order
    context.fired = False

def before_trading(context):
    pass


def handle_bar(context, bar_dict):
    if not context.fired:
        for i in range(len(stocks_list)):
            order_percent(stocks_list[i], stocks_share[i])
        context.fired = True
