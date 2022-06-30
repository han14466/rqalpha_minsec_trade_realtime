# run_func_demo
from rqalpha.apis import *
from rqalpha import run_func


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    context.s1 = "000001.XSHE"
    # 实时打印日志
    logger.info("Interested at stock: " + str(context.s1))
    subscribe(context.s1)


# before_trading此函数会在每天交易开始前被调用，当天只会被调用一次
def before_trading(context, bar_dict):
    pass


def after_trading(context):
    pass


def handle_tick(context,tick):
    order_shares(context.s1, 100)

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！
    # order_shares(context.s1, 1000)
    pass

config = {
    "base": {
        "data_bundle_path": "./bundle_plus",
        "start_date": "20180102",
        "end_date": "20180105",
        "benchmark": "000300.XSHG",
        "run_type": "b",
        "frequency": "tick",
        "accounts": {
            "stock": 100000000,
        }
    },
    "extra": {
        "log_level": "verbose",
    },
    'mod': {
        "sys_analyser": {
            "enabled": True,
            "plot": False,
            "record": True,
            "output_file": "./test.pickle",
            "plot_save_file": "./test.png",
        },
        'stock_realtime': {'enabled': False},
        'sys_progress': {'enabled': True},
        'sys_risk': {'enabled': True},
        'sys_scheduler': {'enabled': True},
        'sys_simulation': {'enabled': True,
                           'matching_type':'last'
                           },
        'sys_transaction_cost': {'enabled': True},
        # 'minute_trade': {
        #     'enabled': True,
        #     'order_book_list': ['000300.XSHG', '000001.XSHE']
        # }
        'tick_trade': {
            'enabled': True
        }
    },
}

# 您可以指定您要传递的参数
run_func(init=init, before_trading=before_trading, handle_tick=handle_tick, config=config)

# 如果你的函数命名是按照 API 规范来，则可以直接按照以下方式来运行
# run_func(**globals())
 