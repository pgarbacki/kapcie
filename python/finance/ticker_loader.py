import abc
import json

from finance.ticker import Ticker

class TickerLoader(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.initialize()

    @abc.abstractmethod
    def initialize(self):
        return

    @abc.abstractmethod
    def load(self, location, symbols=None):
        return

    def _filter(self, tickers, symbols=None):
        if not symbols:
            return tickers
        result = []
        for ticker in tickers:
            if ticker.symbol in symbols:
                result.append(ticker)
        return result


class StringTickerLoader(TickerLoader):
    def initialize(self):
        return

    def load(self, location, symbols=None):
        tickers = []
        sym = location.split(',')
        for symbol in sym:
            ticker = Ticker()
            ticker.symbol = symbol
            tickers.append(ticker)
        return self._filter(tickers, symbols)


class JsonTickerLoader(TickerLoader):
    def initialize(self):
        return

    def load(self, location, symbols=None):
        tickers = []
        with open(location) as f:
            data = json.load(f)
            for item in data:
                ticker = item['Ticker']
                if ticker:
                    # convert from unicode
                    ticker = str(ticker)
                ticker = Ticker(ticker, item['Name'], item['Exchange'],
                    item['categoryName'], item['categoryNr'])
                tickers.append(ticker)
        return self._filter(tickers, symbols)


def load_tickers(options):
    if not options.ticker_file:
        loader = StringTickerLoader()
        return loader.load(options.tickers)
    symbols = None
    if options.tickers:
        symbols = options.tickers.split(',')
    loader = JsonTickerLoader()
    return loader.load(options.ticker_file, symbols)
