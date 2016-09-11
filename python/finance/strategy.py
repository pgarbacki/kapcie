import abc
import datetime

from dateutil.relativedelta import relativedelta

from finance.trade import FixedSharesTrade


class Strategy(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def parse(strategy_args):
        args = strategy_args.split(',')
        result = {}
        for arg in args:
            kv = arg.split(':')
            if len(kv) != 2:
                raise Exception('expected key:value, found', arg)
            result[kv[0]] = kv[1]
        return result

    @abc.abstractmethod
    def trades(self, options):
        return


class FirstOfTheMonthStrategy(Strategy):
    def __init__(self):
        self._tickers = None
        self._start = None
        self._end = None
        self._shares = None

    def _initialize(self, options):
        self._tickers = options['tickers']
        self._start = options['start_date']
        self._end = options['end_date']
        args = Strategy.parse(options['strategy_args'])
        if 'shares' not in args:
            raise Exception('missing shares')
        self._shares = int(args['shares'])

        # if 'start' not in args:
        #     raise Exception('missing start date')
        # self._start = parse(args['start'])
        # if not self._start:
        #     raise Exception('misformatted start date', args['start'])

        # if 'symbol' not in args:
        #     raise Exception('missing symbol')
        # self._symbol = parse(args['symbol'])

        # if 'shares' not in args:
        #     raise Exception('missing shares')
        # self._shares = parse(args['shares'])

    def trades(self, options):
        self._initialize(options)
        sell_date = datetime.datetime(self._start.year, self._start.month,
            self._start.day)
        buy_date = sell_date - datetime.timedelta(days=1)
        if buy_date < self._start:
            sell_date += relativedelta(months=1)
        result = []
        while sell_date < self._end:
            buy_date = sell_date - datetime.timedelta(days=1)
            for ticker in self._tickers:
                result.append(FixedSharesTrade(buy_date, ticker, self._shares))
                result.append(
                    FixedSharesTrade(sell_date, ticker, -self._shares))
            sell_date += relativedelta(months=1)
        return result


_STRATEGIES = {
    'first_of_the_month': FirstOfTheMonthStrategy,
}

def get_trades(options):
    strategy = _STRATEGIES[options['strategy']]()
    return strategy.trades(options)
