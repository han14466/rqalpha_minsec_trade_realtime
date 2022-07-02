# -*- coding: utf-8 -*-
#
# Copyright 2017 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

import pandas as pd

from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.environment import Environment
from rqalpha.model.tick import TickObject
from rqalpha.utils.i18n import gettext as _
from . import data_board


class DirectDataSource(BaseDataSource):
    def __init__(self, path):
        super(DirectDataSource, self).__init__(path, {})
        self._env = Environment.get_instance()

    def get_bar(self, instrument, dt, frequency):
        bar = data_board.realtime_quotes_df.loc[instrument.order_book_id].to_dict()
        return bar

    def current_snapshot(self, instrument, frequency, dt):
        try:
            snapshot_dict = data_board.realtime_quotes_df.loc[instrument.order_book_id].to_dict()
        except KeyError:
            return None
        snapshot_dict["last"] = snapshot_dict["price"]
        snapshot_dict["datetime"] = pd.Timestamp(snapshot_dict["datetime"]).to_pydatetime()
        return TickObject(instrument, snapshot_dict)

    def available_data_range(self, frequency):
        return datetime.date(2017, 1, 1), datetime.date.max


    def history_bars(self, instrument, bar_count, frequency, fields, dt,
                     skip_suspended=True, include_now=False,
                     adjust_type='pre', adjust_orig=None):

        result = None

        if "close" == fields:
            if frequency != '1d' or dt.strftime("%Y%m%d") == datetime.datetime.today().strftime("%Y%m%d"):
                bar = self.get_bar(instrument,dt,frequency)[fields]
                return [bar]
            else:
                import os
                import time
                import logging
                import dataapi

                try:
                    start_date = dt.strftime("%Y%m%d")
                    stock_code = instrument.order_book_id
                    if instrument.type == 'INDX':
                        if stock_code == "000300.XSHG":
                            stock_code = "399300.SZ"
                        else:
                            stock_code = stock_code.replace("XSHE","SH")
                            stock_code = stock_code.replace("XSHG","SZ")

                        logging.info("INDX dataapi get_index_daily_data stock_code:[{stock_code}] start_date:[{start_date}] end_date:[{end_date}]".format(stock_code=stock_code,start_date=start_date,end_date=start_date))
                        daily_data = dataapi.get_index_data(stock_code=stock_code, start_date=start_date,
                                                            end_date=start_date)
                    elif instrument.type == 'CS':
                        stock_code = stock_code.replace("XSHE","SH")
                        stock_code = stock_code.replace("XSHG","SZ")
                        logging.info("CS dataapi get_stock_daily_data stock_code:[{stock_code}] start_date:[{start_date}] end_date:[{end_date}]".format(stock_code=stock_code,start_date=start_date,end_date=start_date))
                        daily_data = dataapi.get_stock_data(stock_code=stock_code, start_date=start_date,
                                                              end_date=start_date)
                    close = daily_data["close"][0]
                    result = [close]
                except:
                    logging.error("dataapi get data error please check")

        if result is None:
            result = super().history_bars(instrument, bar_count, frequency, fields, dt,skip_suspended, include_now, adjust_type, adjust_orig)

        return result

