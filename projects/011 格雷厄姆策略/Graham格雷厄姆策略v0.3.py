import pandas as pd
import numpy as np 

def init(context):

    scheduler.run_monthly(rebalance, 8)
    

    
# before_trading此函数会在每天策略交易开始前被调用，当天只会被调用一次
def before_trading(context):
    
    pass

    
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
                fundamentals.eod_derivative_indicator.pb_ratio < 2)
            .filter(
                fundamentals.eod_derivative_indicator.pe_ratio< 25)
            .filter(
                fundamentals.financial_indicator.inc_earnings_per_share> 0)
            .filter(
                fundamentals.financial_indicator.inc_profit_before_tax > 0)
            .filter(
                fundamentals.financial_indicator.current_ratio > 2)
            .filter(
                fundamentals.financial_indicator.quick_ratio > 1.7)
            .order_by(fundamentals.eod_derivative_indicator.market_cap.desc(
                )).limit(num_stocks))
                
    context.fundamental_df = fundamental_df
    context.stocks = context.fundamental_df.columns.values
    
    if  len(list(context.stocks)) > 0:     
        codes= list(context.stocks)

def rebalance(context, bar_dict):
    
    context.start_date= str(context.now.year - 1)+'-'+str(context.now.month)+'-'+str(context.now.day-1)
    context.end_date= str(context.now.year)+'-'+str(context.now.month)+'-'+str(context.now.day-1)
    logger.info(context.start_date, context.end_date)
    
    stocks= list(context.stocks)
    
    for stock in context.portfolio.positions:
        if stock not in context.fundamental_df:
            order_target_percent(stock, 0)
            logger.info('卖出:%s' % stock)
    
    if len(stocks) > 1:        
        weight = update_weights(context, context.stocks, context.start_date, context.end_date)
        
        for n in range(len(stocks)):
            order_target_percent(stocks[n], weight[n])
                
            logger.info('买入:%s, %s' % (stocks[n], weight[n]))
                
    elif len(stocks) == 1:
        stock = stocks[0]
        order_target_percent(stock, 1)
        


def update_weights(context, stocks, start_date, end_date, frequency= '1d'):

    #导入专用模块scipy.optimize，主要用于最优化问题求解
    import scipy.optimize as sco 
    price= price= get_price(stocks, start_date, end_date, fields= ['close'])
    
    #算出收益率
    rets= np.log(price/ price.shift(1))
    rets.mean()* 252

    #股票池子中股票过去一年的收盘价，算出平均收益和标准差，得到组合的收益、波动和夏普比率
    def statistics(weights):

        weights= np.array(weights)
        pret= np.sum(rets.mean()* weights) * 252
        pvol= np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))

        return np.array([pret, pvol, pret/pvol])

    #最优化问题中的目标函数，我们的目标是夏普比率最大
    def min_func_sharpe(weights):
        return -statistics(weights)[2]

    #约束条件：首先，权重和是1  其次，权重只能在0到1之间取得
    cons= ({'type':'eq', 'fun':lambda x: np.sum(x)-1 })
    bnds= tuple((0, 1) for x in range(len(stocks)))

    opts= sco.minimize(min_func_sharpe, len(stocks) * [1./len(stocks)], bounds=bnds, method='SLSQP', constraints=cons)
    
    #输出最优解中每支股票的权重，进行投资
    return opts['x'].round(3)
    