"""Multiple Correspondence Analysis (MCA)"""
from __future__ import annotations

import numpy as np
import pandas as pd
import sklearn.base
import sklearn.utils

from prince import utils

from . import ca


class MCA(sklearn.base.BaseEstimator, sklearn.base.TransformerMixin, ca.CA):
    def fit(self, X, y=None):
        """Fit the MCA for the dataframe X.

        The MCA is computed on the indicator matrix (i.e. `X.get_dummies()`). If some of the columns are already
        in indicator matrix format, you'll want to pass in `K` as the number of "real" variables that it represents.
        (That's used for correcting the inertia linked to each dimension.)
        """

        if self.check_input:
            sklearn.utils.check_array(X, dtype=[str, np.number])

        # K is the number of actual variables, to apply the Benzécri correction
        self.K_ = X.shape[1]

        # One-hot encode the data
        one_hot = pd.get_dummies(X, columns=X.columns)

        # We need the number of columns to apply the Greenacre correction
        self.J_ = one_hot.shape[1]

        # Apply CA to the indicator matrix
        super().fit(one_hot)

        return self

    def row_coordinates(self, X):
        return super().row_coordinates(pd.get_dummies(X, columns=X.columns))

    def row_cosine_similarities(self, X):
        oh = pd.get_dummies(X, columns=X.columns)
        return super()._row_cosine_similarities(X=oh, F=super().row_coordinates(oh))

    def column_coordinates(self, X):
        return super().column_coordinates(pd.get_dummies(X, columns=X.columns))

    def column_cosine_similarities(self, X):
        oh = pd.get_dummies(X, columns=X.columns)
        return super()._column_cosine_similarities(X=oh, G=super().column_coordinates(oh))

    @utils.check_is_fitted
    def transform(self, X):
        """Computes the row principal coordinates of a dataset."""
        if self.check_input:
            sklearn.utils.check_array(X, dtype=[str, np.number])
        return self.row_coordinates(X)
