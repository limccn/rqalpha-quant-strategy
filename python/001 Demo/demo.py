def init(context):
    logger.info("init")
    context.s1 = "000001.XSHE"
    update_universe(context.s1)
    context.fired = False
    context.cnt = 1

def before_trading(context):
    logger.info("Before Trading", context.cnt)
    context.cnt += 1

def handle_bar(context, bar_dict):
    context.cnt += 1
    logger.info("handle_bar", context.cnt)
    if not context.fired:
        order_percent(context.s1, 1)
        context.fired = True
