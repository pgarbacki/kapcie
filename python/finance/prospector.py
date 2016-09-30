import abc
import datetime
import sys
import time
import tensorflow as tf

from dateutil.parser import parse

from finance.market_loader import load_market
from finance.portfolio import Portfolio
from finance.simulation import Simulation
from finance.strategy import get_trades
from finance.ticker_loader import load_tickers
from finance.linear_regression_estimator import LinearRegressionEstimator


flags = tf.app.flags
FLAGS = flags.FLAGS


flags.DEFINE_string('strategy', 'first_of_the_month', 'strategy to simulate')
flags.DEFINE_string('strategy_args', 'shares:100', 'strategy arguments')
flags.DEFINE_string('tickers', 'SPY', 'comma separated list of tickers')
flags.DEFINE_string('ticker_file', 'Stock.json', 'file with tickers')
flags.DEFINE_string('start_date', '2016-08-01', 'start date')
flags.DEFINE_string('end_date', time.strftime('%Y-%m-%d'), 'end date')
flags.DEFINE_string('model_dir', '/tmp/fin_model', 'model directory')
flags.DEFINE_string('command', 'simulate', 'command to run')


class Command(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def _parse_flags(required):
        result = {}
        result['tickers'] = load_tickers(FLAGS.tickers, FLAGS.ticker_file)
        if 'tickers' in required and 'tickers' not in result:
            raise Exception('missing tickers')

        if FLAGS.start_date:
            start_date = parse(FLAGS.start_date)
            if not start_date:
                raise Exception('misformatted start_date', FLAGS.start_date)
            result['start_date'] = start_date
        if 'start_date' in required and 'start_date' not in result:
            raise Exception('missing start_date')

        if FLAGS.end_date:
            end_date = parse(FLAGS.end_date)
            if not end_date:
                raise Exception('misformatted end_date', FLAGS.end_date)
            result['end_date'] = end_date
        if 'end_date' in required and 'end_date' not in result:
            raise Exception('missing end_date')

        if FLAGS.strategy:
            result['strategy'] = FLAGS.strategy
        if 'strategy' in required and 'strategy' not in result:
            raise Exception('missing strategy')

        if FLAGS.strategy_args:
            result['strategy_args'] = FLAGS.strategy_args
        if 'strategy_args' in required and 'strategy_args' not in result:
            raise Exception('missing strategy_args')

        if FLAGS.model_dir:
            result['model_dir'] = FLAGS.model_dir
        if 'model_dir' in required and 'model_dir' not in result:
            raise Exception('missing model_dir')

        return result

    @abc.abstractmethod
    def execute(self):
        return


class PrintHistory(Command):

    def __init__(self):
        return

    def execute(self):
        options = Command._parse_flags(['tickers', 'start_date', 'end_date'])
        market = load_market(options['start_date'], options['end_date'],
                             options['tickers'])
        for stock in market.stocks.values():
            print(stock)


class Simulate(Command):

    def __init__(self):
        return

    def execute(self):
        options = Command._parse_flags(['tickers', 'start_date', 'end_date',
                                        'strategy'])
        market = load_market(options['start_date'], options['end_date'],
                             options['tickers'])
        portfolio = Portfolio()
        simulation = Simulation(portfolio, market)
        trades = get_trades(options)
        simulation.run(trades)
        print(simulation)


class Train(Command):

    def __init__(self):
        return

    def execute(self):
        options = Command._parse_flags(['tickers', 'start_date', 'end_date',
                                        'model_dir'])
        market = load_market(options['start_date'], options['end_date'],
                             options['tickers'])
        if len(market.stocks) != 1:
            raise Exception('expected 1 stock, found %d' % len(market.stocks))
        stock = next(iter(market.stocks.values()))
        examples = stock.features_all()
        print('DEBUG: examples', examples)
        estimator = LinearRegressionEstimator(options['model_dir'])
        estimator.train(examples, 1000)
        print('trained model written to', options['model_dir'])


_COMMANDS = {
    'print_history': PrintHistory,
    'simulate': Simulate,
    'train': Train,
}


def main(_):
    '''
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
    portfolio = parser.add_argument('-m',
                                    '--model_dir',
                                    dest='model_dir',
                                    default='/tmp/fin_model',
                                    help='model directory')
    parser.add_argument('command',
                        choices=_COMMANDS.keys(),
                        help='command name')
    options = parser.parse_args(sys.argv[1:])
    '''
    command = _COMMANDS[FLAGS.command]()
    command.execute()


if __name__ == '__main__':
    tf.app.run()
