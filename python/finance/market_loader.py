# import matplotlib.pyplot
# import pandas
# import QSTK.qstkutil.tsutil
# from QSTK.qstkutil import DataAccess
# from QSTK.qstkutil import qsdateutil
import abc
import datetime
import pandas.io.data as web

from finance.market import Market
from finance.portfolio import Portfolio
from finance.stock import Stock
from finance.ticker_loader import load_tickers


class MarketLoader(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.initialize()

    @abc.abstractmethod
    def initialize(self):
        return

    @abc.abstractmethod
    def load(self, start, end, time_of_day, tickers):
        return


class WebMarketLoader(MarketLoader):
    # _QUOTE_KEYS = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    def initialize(self):
        return
        # self._data_access = DataAccess.DataAccess('Yahoo')

    def load(self, start, end, tickers):
        # timestamps = qsdateutil.getNYSEdays(start, end, tod)
        # data = self._data_access.get_data(timestamps, tickers, self._QUOTE_KEYS)
        result = Market()
        for ticker in tickers:
            quotes = web.DataReader(ticker.symbol, 'yahoo', start, end)
            stock = Stock(ticker)
            stock.set_quotes(start, end, quotes)
            result.add_stock(stock)
        return result

        # ls_symbols = ["F"]  # ["AAPL", "GLD", "GOOG", "$SPX", "XOM"]
        # dt_start = datetime.datetime(2012, 9, 1)
        # print start, dt_start
        # dt_end = datetime.datetime(2012, 10, 1)
        # dt_timeofday = tod # datetime.timedelta(hours=16)
        # ldt_timestamps = qsdateutil.getNYSEdays(dt_start, dt_end, dt_timeofday)
        # c_dataobj = DataAccess.DataAccess('Yahoo')
        # ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
        # ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
        # print ldf_data
        # self._data = dict(zip(self._QUOTE_KEYS, ldf_data))
        # print self._data


def load_market(options):
    loader = WebMarketLoader()
    return loader.load(options['start_date'], options['end_date'],
        options['tickers'])
