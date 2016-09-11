import abc
import numpy as np

from collections import OrderedDict

from finance.portfolio import Position
from finance.portfolio import Portfolio


class Trade(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def _to_debug_dict(self):
        return

    @abc.abstractmethod
    def execute(self, market, portfolio):
        return

    def _initialize(self, date):
        self.date = date

    def __str__(self):
        return str(self._to_debug_dict())

    def __repr__(self):
        return self.__str__()


class FixedSharesTrade(Trade):
    def __init__(self, date, ticker, shares):
        self._initialize(date)
        if not date:
            raise Exception('empty date')
        if not ticker:
            raise Exception('empty ticker')
        if shares == 0:
            raise Exception('no shares')
        self._ticker = ticker
        self._shares = shares

    def _to_debug_dict(self):
        result = OrderedDict()
        result['date'] = self.date.strftime('%Y-%m-%d')
        result['symbol'] = self._ticker.symbol
        result['shares'] = self._shares
        return str(result)

    def execute(self, market, portfolio):
        result = 0
        price = market.quote(self.date, self._ticker)
        position = None
        if self._ticker in portfolio.positions:
            position = portfolio.positions[self._ticker]
        if self._shares < 0 and position is None:
            raise Exception('symbol', self._ticker.symbol,
                'not found in portfolio', portfolio)
        if position is None:
            position = Position(self._ticker, self._shares, price)
            portfolio.positions[self._ticker] = position
        else:
            position.shares += self._shares
            if position.shares == 0:
                del portfolio.positions[self._ticker]
            else:
                position.price = (position.price * position.shares +
                    price * self._shares) / (position.shares + self._shares)
        portfolio.cash -= self._shares * price
