# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from core import mapper, reducer


class MapReduce(object):
    """DataHandler is an interface to apply MapReduce into retention matrix calculation"""
    def __init__(self, df, periods, dimensions, last_date=None, nature_periods=[]):
        self.df = df
        self.periods = periods
        self.last_date = last_date
        self.nature_periods = nature_periods
        self.dimensions = dimensions

    def get_map_reduce_result(self):
        df_mapper = mapper(self.df, self.periods, self.last_date, self.nature_periods)
        df_reducer = reducer(df_mapper, self.dimensions, self.periods, self.nature_periods)
        return df_reducer
