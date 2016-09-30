import abc

import tensorflow as tf

from finance.feature import Feature


class Estimator(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def _prepare_input(examples):
        # Creates a dictionary mapping from each continuous feature column name (k)
        # to the values of that column stored in a constant Tensor. Exclude the
        # first column that contains the label.
        continuous_cols = {f.name: tf.constant(
            examples[f.name].values) for f in Feature.continuous()
            if f.name in examples and f.name != examples.columns.values[0]}
        # Creates a dictionary mapping from each categorical feature column name (k)
        # to the values of that column stored in a tf.SparseTensor. Exclude the fist
        # column that contains the label.
        categorical_cols = {f.name: tf.SparseTensor(
            indices=[[i, 0] for i in range(examples[f.name].size)],
            values=examples[f.name].values,
            shape=[examples[f.name].size, 1])
            for f in Feature.categorical()
            if f.name in examples and f.name != examples.columns.values[0]}
        # Merges the two dictionaries into one.
        feature_cols = dict(continuous_cols)
        feature_cols.update(categorical_cols)
        # Converts the label column into a constant Tensor.
        label = tf.constant(examples.ix[:, 0].values)
        # Returns the feature columns and the label.
        return feature_cols, label

    @abc.abstractmethod
    def _build(self):
        return

    @abc.abstractmethod
    def _load(self):
        return

    def train(self, examples, steps):
        estimator = self._build()
        estimator.fit(input_fn=lambda: Estimator._prepare_input(
            examples), steps=steps)
        print('DEBUG: weights', estimator.weights_)

    def evaluate(self, examples):
        estimator = self._load()
        results = m.evaluate(
            input_fn=lambda: Estimator._prepare_input(examples), steps=1)
        for key in sorted(results):
            print('%s: %s' % (key, results[key]))
