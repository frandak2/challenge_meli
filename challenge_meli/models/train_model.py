# Importlibraries
import challenge_meli.utils.paths as path
from challenge_meli.utils.meli_utils import get_model_performance_test_set, save_simple_metrics_report, update_model

import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.model_selection import train_test_split, cross_validate

from xgboost import XGBClassifier
rs = {'random_state': 42}

from sklearn.metrics import classification_report
from challenge_meli.utils.logger import get_logging_config

import logging
import logging.config
import warnings

# configurando logging
logging.config.dictConfig(get_logging_config())

# Ignoring warnings
warnings.filterwarnings("ignore")

logging.info('Training Model Start...')

logging.info('Read Data...')
data = pd.read_csv(path.data_processed_dir('data_clean.csv'))

data['condition'].replace(to_replace='used', value=0, inplace=True)
data['condition'].replace(to_replace='new', value=1, inplace=True)

cols_time = ['Hour_created','Min_created','Hour_updated','Min_updated']
data[cols_time] = data[cols_time].astype('category')

# Dividir los datos en variables de entrada y salida
logging.info('Split Data...')
X = data.drop('condition', axis=1)
y = data['condition']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=42)

logging.info('Create pipeline...')
# Select column type
num_cols = [item for item in X_train.select_dtypes(include=['int','float']).columns]
cat_cols = [item for item in  X_train.select_dtypes(include=['string','object','boolean']).columns]

# Crear una pipeline que incluya el ColumnTransformer y el RandomForestClassifier
# Crear un objeto ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(with_mean=False), num_cols),
        ('cat-nominal', OneHotEncoder(), cat_cols)
    ],
    )
pipe = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model',XGBClassifier(**rs))
    ]
)

# realizar validacion cruzada
logging.info('Cross validation...')
final_result = cross_validate(pipe, X_train, y_train, return_train_score=True, cv=5)
#observamos la dispersion del score
train_score_std = np.std(final_result['train_score'])
test_score_std = np.std(final_result['test_score'])
logging.info('Dispersion del score en la validacion cruzada')
logging.info(f'Dispersion train score: {train_score_std}')
logging.info(f'Dispersion test score: {test_score_std}')

# Observamos la media del score
train_score_mean = np.mean(final_result['train_score'])
test_score_mean = np.mean(final_result['test_score'])
logging.info('media del score en la validacion cruzada')
logging.info(f'media train score: {train_score_mean}')
logging.info(f'media test score: {test_score_mean}')

# Entrenar modelo
logging.info('Train model...')
pipe.fit(X_train, y_train)
# Mostrar los resultados

validation_score =pipe.score(X_test, y_test)

y_pred = pipe.predict(X_test)

# Imprimiendo el reporte de clasificación
logging.info('Create report...')
report = classification_report(y_test, y_pred)
logging.info(report)

get_model_performance_test_set('cm_model', y_test, y_pred)

save_simple_metrics_report('report', train_score_mean, test_score_mean, validation_score, report, pipe)
update_model('pipe_model',pipe)
logging.info('Training Model End...')