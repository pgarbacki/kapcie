from collections import OrderedDict


class Simulation(object):
    def __init__(self, portfolio, market):
        if not market:
            raise Exception('empty market')
        self._market = market
        if portfolio:
            self.portfolio = portfolio
        else:
            self.portfolio = Portfolio()

    def run(self, trades):
        trades = sorted(trades, key=lambda trade: trade.date)
        for trade in trades:
            trade.execute(self._market, self.portfolio)

    def __str__(self):
        debug = OrderedDict()
        debug['portfolio'] = self.portfolio
        return str(debug)

    def __repr__(self):
        return self.__str__()
