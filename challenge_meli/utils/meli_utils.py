from sklearn.pipeline import Pipeline
from joblib import dump, load
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

from sklearn.metrics import f1_score,precision_score,recall_score,accuracy_score, confusion_matrix

import challenge_meli.utils.paths as path
rs = {'random_state': 42}

def check_quality(data):
    """Check the quality from data, count the NA, DUPLICATED and unique.
    Args:
        data (DataFrame): DataFrame to check
    """
    # Verificamos la cantidad de valores NA en cada columna
    print("Valores NA por columna:")
    print(data.isna().sum() / data.shape[0] *100)

    # Verificamos la cantidad de datos duplicados en el dataframe
    print("\nCantidad de datos duplicados:")
    print(data.duplicated().sum()/ data.shape[0] *100)

    # Verificamos la cantidad de valores únicos en cada columna
    print("\nValores únicos por columna:")
    print(data.nunique())

def drop_missing_values(data, threshold):
    """Remove cols with NaN

    Args:
        data (DataFrame): DataFrame to clean
        threshold (float): threshold of cleaning

    Returns:
        DataFrame: DataFrame clean
    """
    min_count = int(((100 - threshold) / 100) * data.shape[0] + 1)
    data.dropna(axis=1, thresh=min_count, inplace=True)
    return data


# Classification - Model Pipeline
def modelPipeline(X_train, X_test, y_train, y_test):

    log_reg = LogisticRegression(**rs,solver='saga', max_iter=200)
    mlp = MLPClassifier(max_iter=500, **rs)
    dt = DecisionTreeClassifier(**rs)
    rf = RandomForestClassifier(**rs)
    xgb = XGBClassifier(**rs, verbosity=0)

    # Crear un objeto ColumnTransformer
    # Crear una pipeline que incluya el ColumnTransformer
    # Crear un objeto ColumnTransformer
    num_cols = [item for item in X_train.select_dtypes(include=['int','float']).columns]
    cat_cols = [item for item in  X_train.select_dtypes(include=['string','object','boolean']).columns]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(with_mean=False), num_cols),
            ('cat-nominal', OneHotEncoder(), cat_cols)
        ],
        )

    clfs = [
            ('Logistic Regression', log_reg), 
            ('MLP', mlp), 
            ('Decision Tree', dt), 
            ('Random Forest', rf), 
            ('XGBoost', xgb)
            ]

    pipelines = []

    scores_data = pd.DataFrame(columns=['Model', 'F1_Score', 'Precision', 'Recall', 'Accuracy'])


    for clf_name, clf in clfs:

        pipeline = Pipeline(steps=[
                                   ('preprocessor', preprocessor),
                                   ('classifier', clf)
                                   ]
                            )
        pipeline.fit(X_train, y_train)


        y_pred = pipeline.predict(X_test)
        # F1-Score
        fscore = f1_score(y_test, y_pred,average='weighted')
        # Precision
        pres = precision_score(y_test, y_pred,average='weighted')
        # Recall
        rcall = recall_score(y_test, y_pred,average='weighted')
        # Accuracy
        accu = accuracy_score(y_test, y_pred)


        pipelines.append(pipeline)

        scores_data = scores_data.append({
                                    'Model' : clf_name, 
                                    'F1_Score' : fscore,
                                    'Precision' : pres,
                                    'Recall' : rcall,
                                    'Accuracy' : accu
                                    }, 
                                    ignore_index=True)
        
    return pipelines, scores_data

def update_model(model_name:str, model: Pipeline) -> None:
    """update or create model pkl version.
    Args:
        model_name(str): name of model
        model(Pipeline): pipeline trained
    """
    dump(model, path.models_dir(f'{model_name}.pkl'))

def get_model(model_name:str) -> Pipeline:
    model = load(path.models_dir(f'{model_name}'))
    return model


def save_simple_metrics_report(name_report:str, train_score: float, test_score: float, validation_score: float, report, model: Pipeline) -> None:
    """Create simple report with metrics of performance from Modelo or KPI's and models parameters.
    Args:
        name_report(str): name of report
        train_score(float):score train
        test_score(float):score test
        validation_score(float): score val
        report(): Report of clasification
        model(Pipeline): Model parameters
    """
    with open(path.reports_dir(f'{name_report}'+'.txt'), 'w') as report_file:

        report_file.write('# Model Pipeline Description'+'\n')

        for key, value in model.named_steps.items():
            report_file.write(f'### {key}:{value.__repr__()}'+'\n')

        report_file.write(f'### Train Score: {train_score}'+'\n')
        report_file.write(f'### Test Score: {test_score}'+'\n')
        report_file.write(f'### Validation Score: {validation_score}'+'\n')
        report_file.write(f'### Reporte:\n {report}'+'\n')

def get_model_performance_test_set(fig_name: str, y_real: pd.Series, y_pred: pd.Series) ->None:
    """create a matrix confusion to explored the  model metrics

    Args:
        fig_name (str): name of gigure
        y_real (pd.Series): label target real
        y_pred (pd.Series): label target predicted
    """
    cm = confusion_matrix(y_real, y_pred)
    fig, ax = plt.subplots()
    fig.set_figheight(8)
    fig.set_figwidth(12)
    sns.heatmap(cm, annot=True, fmt='g',cmap='PuRd', ax=ax) 
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(['Used', 'New'])
    ax.yaxis.set_ticklabels(['Used', 'New'])
    fig.savefig(path.reports_figures_dir(f'{fig_name}.png'))