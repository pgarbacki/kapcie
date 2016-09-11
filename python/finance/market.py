class Market(object):
    def __init__(self):
        self.stocks = {}

    def add_stock(self, stock):
        self.stocks[stock.ticker] = stock

    def quote(self, date, ticker):
        if ticker not in self.stocks:
            raise Exception('ticker', ticker, 'not found in market')
        stock = self.stocks[ticker]
        return stock.quote(date)
