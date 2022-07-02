import os
from datetime import date

import numpy as np

from rqalpha.const import INSTRUMENT_TYPE
from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.utils.datetime_func import convert_dt_to_int
from rqalpha.utils.functools import lru_cache
from .storages import MinuteBarStore


class MinuteDataSource(BaseDataSource):

    def __init__(self, env, path):
        super(MinuteDataSource, self).__init__(path, {})
        self._env = env
        self._data_store = None

    def load_store(self):
        def _p(name):
            return os.path.join(self._env.config.base.data_bundle_path, name)

        universe = self._env.get_universe()

        data_store = {}
        for order_book_id in universe:
            if order_book_id not in self._ins_id_or_sym_type_map:
                raise RuntimeError("分钟数据不存在 {}".format(order_book_id))
            elif self._ins_id_or_sym_type_map[order_book_id] not in [INSTRUMENT_TYPE.CS, INSTRUMENT_TYPE.INDX]:
                raise RuntimeError("暂时只支持股票类型tick {}".format(order_book_id))

            path = _p('h5/equities/%s-sample.h5' % order_book_id)
            if not os.path.exists(path):
                raise RuntimeError("分钟数据不存在 {}".format(order_book_id))

            data_store[order_book_id] = MinuteBarStore(path)

        self._data_store = data_store

    def available_data_range(self, frequency):
        return date.min, date.max

    @lru_cache(None)
    def _all_minute_bars_of(self, instrument):
        return self._data_store[instrument.order_book_id].get_bars()

    def get_bar(self, instrument, dt, frequency):
        bars = self._all_minute_bars_of(instrument)

        if len(bars) <= 0:
            return

        dt = np.uint64(convert_dt_to_int(dt))
        pos = bars['datetime'].searchsorted(dt)
        if pos >= len(bars) or bars['datetime'][pos] != dt:
            return None

        return bars[pos]
 