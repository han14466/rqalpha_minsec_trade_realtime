import os
from datetime import date, datetime

import numpy as np
import pandas as pd

from rqalpha.const import INSTRUMENT_TYPE
from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.model.tick import TickObject
from rqalpha.utils.datetime_func import convert_date_to_int
from rqalpha.utils.functools import lru_cache
from .storages import TickBarStore


class TickDataSource(BaseDataSource):

    def __init__(self, env, path):
        super(TickDataSource, self).__init__(path, {})
        self._env = env
        self._data_store = None

    def load_store(self):
        def _p(name):
            return os.path.join(self._env.config.base.data_bundle_path, name)

        universe = self._env.get_universe()

        data_store = {}
        for order_book_id in universe:
            if order_book_id not in self._ins_id_or_sym_type_map:
                raise RuntimeError("tick数据不存在 {}".format(order_book_id))
            elif self._ins_id_or_sym_type_map[order_book_id] not in [INSTRUMENT_TYPE.CS, INSTRUMENT_TYPE.INDX]:
                raise RuntimeError("暂时只支持股票类型tick {}".format(order_book_id))

            path = _p('ticks/%s-sample.h5' % order_book_id)
            if not os.path.exists(path):
                raise RuntimeError("tick数据不存在 {}".format(order_book_id))

            data_store[order_book_id] = TickBarStore(path)

        self._data_store = data_store

    def available_data_range(self, frequency):
        return date.min, date.max

    def get_bar(self, instrument, dt, frequency):
        bars = self._all_day_bars_of(instrument)
        if len(bars) <= 0:
            return
        dt = np.uint64(convert_date_to_int(dt))
        pos = bars['datetime'].searchsorted(dt)
        if pos >= len(bars) or bars['datetime'][pos] != dt:
            return None

        return bars[pos]

    @lru_cache(None)
    def _all_ticks_of(self, order_book_id, date):
        return self._data_store[order_book_id].get_ticks(date)

    def tick_dataframe(self, ticks):
        df = pd.DataFrame(ticks)

        def merge_datetime(_datetime):
            return datetime.strptime(_datetime[:-3], '%Y%m%d%H%M%S')

        df['datetime'] = df['date'].astype(str) + df['time'].astype(str)
        df['datetime'] = df['datetime'].apply(merge_datetime)

        return df

    def get_merge_ticks(self, order_book_id_list, trading_date, last_dt=None):
        merge_ticks = []
        instruments = self.get_instruments(order_book_id_list)
        for ins in instruments:
            ticks = self._all_ticks_of(ins.order_book_id, trading_date.strftime('%Y%m%d'))
            if len(ticks) <= 0:
                continue

            df = self.tick_dataframe(ticks)
            for index in df.index:
                merge_ticks.append(TickObject(ins, {
                    'time': df['time'][index],
                    'last': df['last'][index],
                    'high': df['high'][index],
                    'low': df['low'][index],
                    'volume': df['volume'][index],
                    'open_interest': df['open_interest'][index],
                    'total_turnover': df['total_turnover'][index],
                    'asks': [df['a1'][index], df['a2'][index], df['a3'][index], df['a4'][index], df['a5'][index]],
                    'bids': [df['b1'][index], df['b2'][index], df['b3'][index], df['b4'][index], df['b5'][index]],
                    'ask_vols': [df['a1_v'][index], df['a2_v'][index], df['a3_v'][index], df['a4_v'][index],
                                 df['a5_v'][index]],
                    'bid_vols': [df['b1_v'][index], df['b2_v'][index], df['b3_v'][index], df['b4_v'][index],
                                 df['b5_v'][index]],
                    'datetime': df['datetime'][index],
                }))

        return merge_ticks
 