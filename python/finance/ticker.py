class Ticker(object):
    def __init__(self, symbol, name=None, exchange=None, category_name=None,
            category_number=None):
        if not symbol:
            raise Exception('empty symbol')
        self.symbol = symbol
        self.name = name
        self.exchange = exchange
        self.category_name = category_name
        self.category_number = category_number

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.__str__()
