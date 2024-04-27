import os
from typing import List, Tuple, Union

import joblib
import numpy as np
import pandas as pd
from xgboost import XGBClassifier

from .constants import THRESHOLD_IN_MINUTES, TOP_10_FEATURES
from .utils import get_min_diff, get_period_day, is_high_season


class DelayModel:

    def __init__(self):
        self._model = None  # Model should be saved in this attribute.
        self._model_path = "./model.pkl"
        self._model_cache = True

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None,
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        data["period_day"] = data["Fecha-I"].apply(get_period_day)
        data["high_season"] = data["Fecha-I"].apply(is_high_season)
        data["min_diff"] = data.apply(get_min_diff, axis=1)
        data["delay"] = np.where(data["min_diff"] > THRESHOLD_IN_MINUTES, 1, 0)
        features = pd.concat(
            [
                pd.get_dummies(data["OPERA"], prefix="OPERA"),
                pd.get_dummies(data["TIPOVUELO"], prefix="TIPOVUELO"),
                pd.get_dummies(data["MES"], prefix="MES"),
            ],
            axis=1,
        )
        features = features[TOP_10_FEATURES]
        if target_column is not None:
            return features, data[["delay"]]
        return features

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame,
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        if os.path.exists(self._model_path):
            return
        n_y0 = target.value_counts()[0]
        n_y1 = target.value_counts()[1]
        scale = n_y0 / n_y1
        model = XGBClassifier(
            random_state=1,
            learning_rate=0.01,
            scale_pos_weight=scale,
        )
        model.fit(features, target)
        self._model = model
        if self._model_cache:
            joblib.dump(self._model, self._model_path)

    def predict(
        self,
        features: pd.DataFrame,
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        if self._model_cache:
            if os.path.exists(self._model_path):
                self._model = joblib.load(self._model_path)
        if self._model is None:
            raise Exception("model is not fitted")
        predictions = self._model.predict(features)
        return predictions.tolist()
