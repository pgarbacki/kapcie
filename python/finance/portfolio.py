import pprint

from collections import OrderedDict

class Position(object):
    def __init__(self, ticker, shares, price):
        self.ticker = ticker
        self.shares = shares
        self.price = float(price)

    def value(self):
        return self.shares * self.price

    def merge(self, position):
        assert self.ticker == position.ticker
        self.price = (self.price * self.shares +
            position.price * position.shares) / (self.shares + position.shares)
        self.shares += position.shares

    def diff(self, position):
        # self - position
        assert self.ticker == position.ticker
        shares = self.shares - position.shares
        price = (self.price * self.shares -
            position.price * position.shares) / shares
        return Position(self.ticker, shares, price)

    def __str__(self):
        debug = OrderedDict()
        debug['ticker'] = self.ticker
        debug['shares'] = self.shares
        debug['price'] = self.price
        return pprint.pformat(debug)

    def __repr__(self):
        return self.__str__()


class Portfolio(object):
    def __init__(self):
        self.cash = 0
        self.positions = {}

    # def merge(self, portfolio):
    #     self.cash += portfolio.cash
    #     for position in portfolio.values():
    #         if position.ticker in self.positions:
    #             self.positions[position.ticker].merge(position)
    #         else:
    #             self.positions[position.ticker] = position

    def value(self):
        result = self.cash
        for position in self.positions.values():
            result += position.value()
        return result

    def __str__(self):
        debug = OrderedDict()
        debug['cash'] = self.cash
        debug['positions'] = self.positions
        return pprint.pformat(debug)

    def __repr__(self):
        return self.__str__()
