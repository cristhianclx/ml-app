### model

We need to choose a model that can predict delays.
Critical metric we are trying to predict is delay=1, because we are trying to identify delays.
Taking that in mind best model is **XGBoost with Feature Importance and with Balance** with f1-score 0.37 (higher than other models) for delay=1.
We are trying to use this in a practical scenario (production) where we try to get better handling of delays.
For model.py, I added `preprocess`, `fit` and `train` methods.
Also I added a `model_path` variable, to only process first time, save to disk and use same file next time.


### api

Using DelayModel, I completed predict EP, this is core of our API.
This predict EP takes a dictionary, we are using Pydantic validation to have data clean. I added a schema for this (using tuples with Literal).
If validation is failing it raises 400 HTTP error, using FastAPI validation.
Also, I added `normalize` function to normalize data that I can pass to model.


### infrastructure

I added a folder called `infrastructure` in this folder I did a setup with terraform to deploy in GCP using Cloud Run.
Also, I added GCP Artifact Registry to store docker image that I'm generating each time.
And to manage DNS, I added a mapped domain in Cloud Run.
For better performance I added cloud storage to manage model generated, so we don't generate each time.


### pipelines

For pipelines in CI, I added a test step and a infrastructure-plan (using terraform) to see what is going to happen in PR. This will happen only in main branch.
For pipelines in CD, I added a test step, infrastructure, create a docker image, push to Google Artifact Registry and update service in Cloud Run. This will happen in PR to main branch.


### stress

Added URL `https://server.ml-app.demo.pe` to manage stress test, Cloud Run with concurrency of 100.


### extras

Added some basic validations and linters (black, flake8, isort).
Added pre-commit rules and pre-commit hooks.
Update requirements to latest versions (it's better to be updated for security fixes).
Added Dockerfile and docker-compose for management: `docker-compose run --service-ports api`.
Added terraform with GCP to manage infrastructure.
