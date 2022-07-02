本项目做了几个更改：
1 基于开源rqalpha4.0版本，支持分钟和tick级别的回测
	增加了两个mod，：rqalpha_mod_minute_trade（\rqalpha4_min_tick_trade_mod\minute_trade\rqalpha_mod_minute_trade）和rqalpha_mod_tick_trade（\rqalpha4_min_tick_trade_mod\tick_trade\rqalpha_mod_tick_trade）。当你按照rqalpha的h5格式存放你的分钟和tick数据时，就可以支持分钟和tick级别的回测
2 基于开源rqalpha3.4版本支持模拟交易的功能
	2.1需要用rqalpha3.4_patch下面的文件覆盖原有的rqalpha3.4的文件
cp -rd ./rqalpha3.4_patch/disk_persist_provider.py /rqalpha_home/rqalpha/utils/
cp -rd ./rqalpha3.4_patch/asset_position.py /rqalpha_home/rqalpha/mod/rqalpha_mod_sys_accounts/position_model/
    2.2 改写rqalpha_mod_stock_realtime,并且需要你有本地的历史指数和股票数据。因为rqalpha做模拟的时候有些条件下会需要历史history_bar,你可以不使用dataapi，但是你需要找到rqalpha相应的函数。

