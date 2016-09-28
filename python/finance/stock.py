from collections import OrderedDict
from enum import Enum
import numpy as np
import pandas as pd
import pprint

from finance.feature import Feature, get_example, FeatureArgs


class Stock(object):

    def __init__(self, ticker):
        if not ticker:
            raise Exception('empty ticker')
        self.ticker = ticker
        self._start = None
        self._end = None
        self._quotes = None

        self._statements = None

    def set_quotes(self, start, end, quotes):
        self._start = start
        self._end = end
        self._quotes = quotes

    def quote(self, date):
        if date < self._start or date > self._end:
            raise Exception('date', date, 'out of range', self._start,
                            self._end)
        rows = self._quotes.loc[self._quotes.index <= date]
        if rows.empty:
            raise Exception('date', date, 'not found')
        i = np.argmin(date - rows.index.to_pydatetime())
        return self._quotes.iloc[i]['Adj Close']

    def _features(self, features):
        result = None
        for date in self._quotes.index:
            example = get_example(FeatureArgs(features, date, self._quotes))
            if result is None:
                result = example
            else:
                result = result.append(example)  # , ignore_index=True)
        return result

    def features_all(self):
        return self._features([feature for feature in Feature])

    def to_debug_dict(self):
        result = OrderedDict()
        result['symbol'] = self.ticker.symbol
        result['start'] = self._start.strftime('%Y-%m-%d')
        result['end'] = self._end.strftime('%Y-%m-%d')
        result['quotes'] = self._quotes
        return result

    def __str__(self):
        return pprint.pformat(self.to_debug_dict())

    def __repr__(self):
        return self.__str__()
