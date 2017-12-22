import pandas as pd
import numpy as np 
import datetime
import math

def init(context):
    date= pd.date_range(start='20150101', end='20170101', freq='B')
    date_index= []
    for d in date:
        date_index.append(datetime.datetime.strftime(d, '%Y-%m-%d'))
    
    context.date_index= date_index    
    scheduler.run_monthly(rebalance, 8)
    
def handle_bar(context, bar_dict):
    
    pass

def before_trading(context):
    
    num_stocks = 10
    
    fundamental_df = get_fundamentals(
        query(
            fundamentals.eod_derivative_indicator.pb_ratio,
            fundamentals.eod_derivative_indicator.pe_ratio,
            fundamentals.financial_indicator.inc_earnings_per_share,
            fundamentals.financial_indicator.inc_profit_before_tax,
            fundamentals.financial_indicator.quick_ratio,
            fundamentals.financial_indicator.current_ratio
            )
            .filter(
                fundamentals.eod_derivative_indicator.pb_ratio< 2)
            .filter(
                fundamentals.eod_derivative_indicator.pe_ratio< 25)
            .filter(
                fundamentals.financial_indicator.inc_earnings_per_share> 0)
            .filter(
                fundamentals.financial_indicator.inc_profit_before_tax > 0)
            .filter(
                fundamentals.financial_indicator.current_ratio > 2)
            .filter(
                fundamentals.financial_indicator.quick_ratio > 1)
            .order_by(fundamentals.eod_derivative_indicator.market_cap.desc(
                )).limit(num_stocks))
                
    context.fundamental_df = fundamental_df
    context.stocks = context.fundamental_df.columns.values
    data= pd.DataFrame(columns= list(context.stocks), index= context.date_index)
    
    if  len(list(context.stocks)) > 0:     
        codes= list(context.stocks)
        logger.info(codes)

def rebalance(context, bar_dict):
    
    stocks= list(context.stocks)
    
    for stock in context.portfolio.positions:
        if stock not in context.fundamental_df:
            order_target_percent(stock, 0)
            logger.info('卖出:%s' % stock)
        
    if len(stocks) > 1:        
        weight = update_weights(context, context.stocks)
    
        for n in range(len(stocks)):
            order_target_percent(stocks[n], weight[n])
            
            logger.info('买入:%s, %s' % (stocks[n], weight[n]))
            
    elif len(stocks) == 1:
        stock = stocks[0]
        order_target_percent(stock, 1)
        
def update_weights(context, stocks, start_date='2013-01-01', end_date='2015-01-01', frequency= '1d'):
    
    '''Return optimize weight.
    
    Parameters
    ==========
    stocks:list
        portfolio stocks
    start_date:str
        default '2015-01-01'
    end_date:str
        default '2016-01-01'
    frequency:str
        '1w','1d','1m','1y'
        default '1d'
        
    Returns
    =======
    weights of stocks
    '''

    import scipy.optimize as sco
    price= price= get_price(stocks, start_date, end_date, fields= ['close'])
    
    rets= np.log(price/ price.shift(1))
    rets.mean()* 252

    #投资组合优化
    def statistics(weights):
        '''Rrturn portfolio statistics.
        Parameters
        ==========
        weights:array-like
            weights for different securities in portfolio

        Returns
        =======
        pret:float
            expected portfolio return
        pvol:float
            expected portfolio volatility
        pret/ pvol: float
            Sharpe ratio for rf= 0
        '''

        weights= np.array(weights)
        pret= np.sum(rets.mean()* weights) * 252
        pvol= np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))

        return np.array([pret, pvol, pret/pvol])

    rets= np.log(price/ price.shift(1))
    rets.mean()* 252

    def min_func_sharpe(weights):
        return -statistics(weights)[2]

    cons= ({'type':'eq', 'fun':lambda x: np.sum(x)-1 })
    bnds= tuple((0, 1) for x in range(len(stocks)))

    opts= sco.minimize(min_func_sharpe, len(stocks) * [1./len(stocks)], bounds=bnds, method='SLSQP', constraints=cons)

    return opts['x'].round(3)