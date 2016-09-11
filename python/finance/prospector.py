import abc
import argparse
import datetime
import sys
import time

from dateutil.parser import parse

from finance.market_loader import load_market
from finance.portfolio import Portfolio
from finance.simulation import Simulation
from finance.strategy import get_trades
from finance.ticker_loader import load_tickers


class Command(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def _parse(options, required):
        result = {}
        result['tickers'] = load_tickers(options)
        if 'tickers' in required and 'tickers' not in result:
            raise Exception('missing tickers')

        if options.start_date:
            start_date = parse(options.start_date)
            if not start_date:
                raise Exception('misformatted start_date', options.start_date)
            result['start_date'] = start_date
        if 'start_date' in required and 'start_date' not in result:
            raise Exception('missing start_date')

        if options.end_date:
            end_date = parse(options.end_date)
            if not end_date:
                raise Exception('misformatted end_date', options.end_date)
            result['end_date'] = end_date
        if 'end_date' in required and 'end_date' not in result:
            raise Exception('missing end_date')

        if options.strategy:
            result['strategy'] = options.strategy
        if 'strategy' in required and 'strategy' not in result:
            raise Exception('missing strategy')

        if options.strategy_args:
            result['strategy_args'] = options.strategy_args
        if 'strategy_args' in required and 'strategy_args' not in result:
            raise Exception('missing strategy_args')

        return result

    @abc.abstractmethod
    def execute(self, options):
        return


class PrintHistory(Command):
    def __init__(self):
        return

    def execute(self, options):
        options = Command._parse(options, ['tickers', 'start_date', 'end_date'])
        market = load_market(options)
        for stock in market.stocks.values():
            print stock


class Simulate(Command):
    def __init__(self):
        return

    def execute(self, options):
        options = Command._parse(options, ['tickers', 'start_date', 'end_date',
            'strategy'])
        market = load_market(options)
        portfolio = Portfolio()
        simulation = Simulation(portfolio, market)
        trades = get_trades(options)
        simulation.run(trades)
        print simulation


def run_command(options):
    command = _COMMANDS[options.command]()
    command.execute(options)


_COMMANDS = {
    'print_history': PrintHistory,
    'simulate': Simulate,
}


def main():
    parser = argparse.ArgumentParser(description='Financial analysis.')
    parser.add_argument('-s',
                        '--strategy',
                        dest='strategy',
                        default='first_of_the_month',
                        help='strategy to simulate')
    parser.add_argument('-sa',
                        '--strategy_args',
                        dest='strategy_args',
                        default='shares:100',
                        help='strategy to simulate')
    parser.add_argument('-t',
                        '--tickers',
                        dest='tickers',
                        default='SPY',
                        help='comma separated list of tickers')
    parser.add_argument('-tf',
                        '--ticker_file',
                        dest='ticker_file',
                        default='Stock.json',
                        help='file with tickers')
    parser.add_argument('-st',
                        '--start_date',
                        dest='start_date',
                        default='2010-08-01',
                        help='start date')
    portfolio = parser.add_argument('-en',
                        '--end_date',
                        dest='end_date',
                        default=time.strftime('%Y-%m-%d'),
                        help='end date')
    parser.add_argument('command',
                        choices=_COMMANDS.keys(),
                        help='command name')
    options = parser.parse_args(sys.argv[1:])
    run_command(options)


if __name__ == '__main__':
    main()
