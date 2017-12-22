import pandas as pd
import numpy as np 
from datetime import datetime
from datetime import timedelta

def init(context):
    
    scheduler.run_monthly(rebalance, 8) 
    scheduler.run_weekly(stoploss, 1) #如果损失超过10%，卖出
    scheduler.run_daily(reinvest) #空闲资金购买A级基金
    context.fja_list= ['150283.XSHE','150249.XSHE','502007.XSHG','150259.XSHE','150217.XSHE','150245.XSHE','502049.XSHG','150241.XSHE','150231.XSHE','150257.XSHE','150169.XSHE','150177.XSHE','150243.XSHE','150329.XSHE','150051.XSHE','150179.XSHE','150186.XSHE','150255.XSHE','150171.XSHE','150315.XSHE','150227.XSHE','150018.XSHE','150237.XSHE','150235.XSHE','150279.XSHE','150305.XSHE','150181.XSHE','502004.XSHG','150229.XSHE','150173.XSHE','150277.XSHE','150200.XSHE','150209.XSHE','150194.XSHE','150273.XSHE','150184.XSHE','150205.XSHE','150309.XSHE','150275.XSHE','150269.XSHE']

    
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
    

def rebalance(context, bar_dict):
    
    stocks= list(context.stocks)    
    
    lastday= context.now +timedelta(days= -1)
    
    #这里会出现问题，就是上年不是闰年，却2月29
    if lastday.month==2 and lastday.day == 29:
        context.start_date= str(lastday.year - 1)+'-'+str(lastday.month)+'-'+str(lastday.day-1)
    else:
        context.start_date= str(lastday.year - 1)+'-'+str(lastday.month)+'-'+str(lastday.day)
    context.end_date= str(lastday.year)+'-'+str(lastday.month)+'-'+str(lastday.day)
    
    for stock in context.portfolio.positions:
        if stock not in stocks:
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
    price= get_price(stocks, start_date, end_date, fields= ['close'])
    
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
    
def stoploss(context, bar_dict):
    
    for stock in context.portfolio.positions:
        if context.portfolio.positions[stock].market_value/context.portfolio.positions[stock].bought_value < 0.9:
            order_target_percent(stock, 0)
            logger.info('%s损失超过0.1，卖出' % stock)

def reinvest(context, bar_dict):            
    cash = context.portfolio.cash
    min_stock= '150283.XSHE'
    min_discount= 0
        
    if cash > 0:
        fja= []
        for stock in context.fja_list:
            if bar_dict[stock].is_trading:
              fja.append(stock)  
        for stock in fja:
            try:
                if bar_dict[stock].discount_rate < min_discount:
                    min_stock= stock
                    min_discount= bar_dict[stock].discount_rate
            except:
                min_stock= stock
                min_discount= 0
        order_target_value(min_stock, cash)
        logger.info('买入%s,当前资产组合为%s' % (stock, str(context.portfolio.positions)))