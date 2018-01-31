from rqalpha.api import *

def init(context):
    logger.info("init")
    context.s1 = ["002024.XSHE","600690.XSHG","601633.XSHG","601933.XSHG"]
    update_universe(context.s1)
    # 是否已发送了order
    context.fired = False

def before_trading(context):
    pass


def handle_bar(context, bar_dict):
    if not context.fired:
        order_percent(context.s1[0], 0.25)
        order_percent(context.s1[1], 0.25)
        order_percent(context.s1[2], 0.25)
        order_percent(context.s1[3], 0.25)
        context.fired = True
