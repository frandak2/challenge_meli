# Challenge_MELI

In this challenge, I was provided with data in JSON format and tasked with developing a machine learning model to predict whether an article is new or used, based on the information provided in the data.

## Tasks Performed
Below are the tasks I completed to develop this machine learning model:

1. Feature Engineering: I performed feature engineering to create new features from the features provided in the data. For example, I created a feature to represent the sizes of the article and another feature to represent the information of the article.

2. Exploratory Data Analysis (EDA): I conducted exploratory data analysis to better understand the distributions of the features and to identify any outliers or missing values.

3. Data Creation: I split the data into training and test sets and converted them into appropriate formats for model training.

4. Model Training: I trained several binary classification models, using different machine learning algorithms to achieve the best possible results.

5. Model Evaluation: I evaluated the performance of the models using different metrics, such as precision, recall, and F1 score, and selected the model that showed the best overall performance.

6. Model Saving: I saved the selected model to a file for future use.

7. API Creation with FastAPI: I created an API using FastAPI, a Python library for API creation. This API receives an HTTP request that includes the article information and returns an HTTP response that indicates whether the article is new or used.

8. API Testing: I conducted tests on the API to ensure that it worked correctly and produced accurate results.

9. Dockerfile Creation: I created a Dockerfile to package the API and its dependencies into a Docker container that can be easily deployed in different environments.

## Conclusions
In summary, in this challenge, I completed a variety of tasks to develop a machine learning model to classify articles as new or used. I also developed an API to implement this model in a production environment and created a Dockerfile to facilitate deployment in different environments.
  
## Installation guide

Please read [install.md](install.md) for details on how to set up this project.

## Project Organization

    ├── LICENSE
    ├── tasks.py           <- Invoke with commands like `notebook`.
    ├── README.md          <- The top-level README for Data Scientist using this project.
    ├── install.md         <- Detailed instructions to set up this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries.
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-fmh-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures         <- Generated graphics and figures to be used in reporting.
    │
    ├── environment.yml    <- The requirements file for reproducing the analysis environment.
    │
    ├── .here              <- File that will stop the search if none of the other criteria
    │                         apply when searching head of project.
    │
    ├── setup.py           <- Makes project pip installable (pip install -e .)
    │                         so challenge_meli can be imported.
    │
    └── challenge_meli               <- Source code for use in this project.
        ├── __init__.py    <- Makes challenge_meli a Python module.
        │
        ├── data           <- Scripts to download or generate data.
        │   └── make_dataset.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling.
        │   └── build_features.py
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │   │                 predictions.
        │   ├── predict_model.py
        │   └── train_model.py
        │
        ├── utils          <- Scripts to help with common tasks.
            └── paths.py   <- Helper functions to relative file referencing across project.
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations.
            └── visualize.py

---
Project based on the [cookiecutter conda data science project template](https://github.com/frandak2/cookiecutter-personal).