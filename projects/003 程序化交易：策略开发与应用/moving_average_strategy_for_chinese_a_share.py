import talib

def init(context):
    # initial operation
#   print ('init entered')
    context.s1 = '600519.XSHG'    #  600519.XSHG Kuichow Moutai
    context.AvgLen1 = 5    # EMA1
    context.AvgLen2 = 20    # EMA2
    context.AvgLen3 = 60    # EMA3
    context.RLength = 4    # daily changed price range 
    context.High = 0.0
    context.Low = 0.0
    
#    print ('init finished')
    
def before_trading(context):
    # do something before daily trading session start
#    print ('before_trading entered')
    # noup
#    print ('before_trading finished')
    pass

def compute_data(context, bar_dict):
    # compute historical data for analysing and trading
    Data = history_bars(context.s1, context.AvgLen3, 
                        '1d', ['close', 'high', 'low'], 
                        skip_suspended=True, include_now=False)  
    Close = Data['close']
    # price changing range
    Range = Data['high'] - Data['low']   
    
    High = Data['high'][-1]
    Low = Data['low'][-1]
    
    #  compute MAs using TA-lib
    EMA1 = talib.EMA(Close, context.AvgLen1)[-1]
    EMA2 = talib.EMA(Close, context.AvgLen2)[-1]
    EMA3 = talib.EMA(Close, context.AvgLen3)[-1]
    #  compute range using TA-lib
    RangeL = talib.SMA(Range[-context.RLength:], context.RLength)[-1]

    return EMA1, EMA2, EMA3, RangeL, High, Low
     
def handle_bar(context, bar_dict):
    # handle every daily bar data
#    print ('handle_bar entered')
        
    # holdings quantity in current portfolio
    cur_position = context.portfolio.positions[context.s1].quantity
    # quantity cash available for buying, 100 share per unit
    shares = int(context.portfolio.cash / bar_dict[context.s1].close/100)*100
    
#    print (cur_position)
#    print (shares)
    
    # compute technical indicators
    EMA1, EMA2, EMA3, RangeL, High, Low = compute_data(context, bar_dict)
    
    # ma golden cross, All in
    if (EMA1 > EMA2 > EMA3) and (shares >0): 
            order_shares(context.s1, shares)
            context.Low = Low
            print('Buy signal, All in')
    
    # dead cross or ma start crossing down 
    if (EMA1 < EMA2) or (EMA1 < (context.Low + RangeL)): 
            order_target_value(context.s1, 0)
            print('Sell signal, All out') 
    
#    print ('handle_bar finished')
    
def after_trading(context):
    # do something after daily trading session finish
#    print ('after_trading entered')
    # noup
#    print ('after_trading finished')
    pass