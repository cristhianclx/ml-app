### choose model

We need to choose a model that can predict delays.
Critical metric we are trying to predict is delay=1, because we are trying to identify delays.
Taking that in mind best model is **XGBoost with Feature Importance and with Balance** with f1-score 0.37 (higher than other models) for delay=1.
We are trying to use this in a practical scenario (production) where we try to get better handling of delays.
For model.py, I added `preprocess`, `fit` and `train` methods.
Also I added a `model_path` variable, to only process first time, save to disk and use same file next time.

### extras

Added some basic validations and linters (black, flake8, isort).
Added pre-commit rules and pre-commit hooks.
