import tensorflow as tf

from finance.estimator import Estimator
from finance.feature import Feature


class LinearRegressionEstimator(Estimator):

    def __init__(self, model_dir):
        self._model_dir = model_dir

    def _build(self):
        columns = []
        # Continuous base features.
        # columns.append(tf.contrib.layers.real_valued_column(
        #     Feature.ADJ_CLOSE_QUOTE.name))
        columns.append(tf.contrib.layers.real_valued_column(
            Feature.PREVIOUS_ADJ_CLOSE_QUOTE.name))

        # Categorical base features.
        columns.append(tf.contrib.layers.sparse_column_with_keys(
            column_name=Feature.DAY_OF_WEEK.name,
            keys=[str(i) for i in range(7)]))
        columns.append(tf.contrib.layers.sparse_column_with_keys(
            column_name=Feature.DAY_OF_MONTH.name,
            keys=[str(i) for i in range(1, 32)]))

        return tf.contrib.learn.LinearRegressor(model_dir=self._model_dir,
                                                feature_columns=columns)

    def _load(self):
        return None
