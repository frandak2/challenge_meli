""""
This script loads data from a JSON file, cleans it by dropping missing values
and flattening nested columns, expands picture data, and saves the cleaned data
to a CSV file. The cleaned data is a subset of the original data containing
the last 10,000 rows. The data is saved in the 'data_processed' directory
using the name 'data_raw.csv'.

"""
import json
import numpy as np
import pandas as pd
import challenge_meli.utils.paths as path
from challenge_meli.utils.meli_utils import drop_missing_values
from challenge_meli.utils.logger import get_logging_config

import logging
import logging.config
import warnings

# configurando logging
logging.config.dictConfig(get_logging_config())

# Ignoring warnings
warnings.filterwarnings("ignore")

def load_data():
    data = pd.read_json(path.data_raw_dir("MLA_100k.jsonlines"), lines=True).tail(10000)
    return data

def check_cols_with_list(data):
    dict_list_cols = [col for col in data.columns if data[col].apply(lambda x: type(x) in [list, dict]).any()]
    drop_cols = []
    for col in dict_list_cols:
        exist_values = data[col].apply(lambda x: 0 if not x else 1)
        if sum(exist_values)<=8000:
            drop_cols.append(col)
    data.drop(columns=drop_cols,inplace=True)
    return data

def flatten_columns(data):
    dict_list_cols = [col for col in data.columns if data[col].apply(lambda x: type(x) in [dict]).any()]
    df_dict = pd.DataFrame()
    for col in dict_list_cols:
        json_open = data[col].apply(lambda x: json.dumps(x))
        df = pd.json_normalize(json_open.apply(json.loads)).add_prefix(col + '_')
        df.replace(to_replace=[''], value=np.nan, inplace=True)
        df_dict = pd.concat([df_dict, df], axis=1)
        data.drop(columns=[col], inplace=True)
    return df_dict

def expand_pictures_column(data):
    temp = pd.DataFrame()
    for row in range(0, 10000):
        if not data['pictures'].iloc[row]:
            pictures = pd.DataFrame(np.nan, index=[0], columns=['pictures_size', 'pictures_secure_url', 'pictures_max_size','pictures_url', 'pictures_quality', 'pictures_id'])
            pictures['index'] = data['index'].iloc[row]
            temp = pd.concat([temp, pictures],ignore_index=True)
        else:
            pictures = pd.DataFrame(data['pictures'].iloc[row]).add_prefix('pictures' + '_').drop_duplicates()
            pictures['index'] = data['index'].iloc[row]
            temp = pd.concat([temp, pictures],ignore_index=True)
    data.drop(columns='pictures', inplace=True)
    data = data.set_index('index').join(temp.set_index('index'), how='inner')
    return data

def clean_data(data):
    data.reset_index(inplace=True)
    logging.info('Drop missing cols...')
    data = drop_missing_values(data, 70.0)
    data = check_cols_with_list(data)
    logging.info('flatten data...')
    df_dict = flatten_columns(data)
    df_dict = drop_missing_values(df_dict, 70.0)
    df_dict = check_cols_with_list(df_dict)
    data = pd.concat([data, df_dict], axis=1)
    data = expand_pictures_column(data)
    data.drop(columns='descriptions', inplace=True)
    logging.info('Data ready...')
    return data

def main():
    logging.info('Make Data Start...')
    logging.info('Loading Data...')
    data = load_data()
    logging.info('Clean Data start...')
    data = clean_data(data)
    logging.info('Clean Data End...')
    data.to_csv(path.data_processed_dir('data_raw.csv'), index=False)
    logging.info('Make Data End...')

if __name__ == '__main__':
    main()