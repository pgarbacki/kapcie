from collections import OrderedDict
from enum import Enum, unique
import datetime
import numpy as np
import pandas as pd
import pprint


@unique
class Feature(Enum):
    ADJ_CLOSE_QUOTE = 1
    PREVIOUS_ADJ_CLOSE_QUOTE = 2
    DAY_OF_WEEK = 3
    DAY_OF_MONTH = 4

    @staticmethod
    def categorical():
        return [Feature.DAY_OF_WEEK, Feature.DAY_OF_MONTH]

    @staticmethod
    def continuous():
        return [Feature.ADJ_CLOSE_QUOTE, Feature.PREVIOUS_ADJ_CLOSE_QUOTE]


class FeatureArgs(object):

    def __init__(self, features, date, quotes):
        if date not in quotes.index:
            raise Exception('date', date, 'not found in', quotes.index)
        self.features = features
        self.date = date
        self.quotes = quotes

    def __str__(self):
        result = OrderedDict()
        result['features'] = self.features
        result['date'] = self.date
        result['quotes'] = self.quotes
        return pprint.pformat(result)

    def __repr__(self):
        return self.__str__()


def _get_adj_close_quote(args):
    return args.quotes.loc[args.date]['Adj Close']


def _get_previous_adj_close_quote(args):
    previous_date = args.date - datetime.timedelta(days=1)
    rows = args.quotes.loc[args.quotes.index <= previous_date]
    if rows.empty:
        return 0
    i = np.argmin(previous_date - rows.index.to_pydatetime())
    return args.quotes.iloc[i]['Adj Close']


def _get_day_of_week(args):
    return str(args.date.weekday())


def _get_day_of_month(args):
    return str(args.date.day)


_FEATURE_EXTRACTORS = {
    Feature.ADJ_CLOSE_QUOTE: _get_adj_close_quote,
    Feature.PREVIOUS_ADJ_CLOSE_QUOTE: _get_previous_adj_close_quote,
    Feature.DAY_OF_WEEK: _get_day_of_week,
    Feature.DAY_OF_MONTH: _get_day_of_month,
}


def get_example(args):
    return pd.DataFrame(
        [[_FEATURE_EXTRACTORS[feature](args) for feature in args.features]],
        columns=[feature.name for feature in args.features],
        index=[args.date])
