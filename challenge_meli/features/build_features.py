"""
The code imports necessary libraries, loads a raw data CSV file into a Pandas dataframe,
cleans and transforms the data by removing irrelevant columns and rows,
dealing with missing values, and extracting new features, and then saves the cleaned data to a new CSV file.
Specifically, it removes rows with more than 50% missing values,
converts the 'date_created' column to a datetime object and extracts month name,
day name, hour, and minute, and removes several irrelevant columns.
It also removes rows with missing values, removes more irrelevant columns,
removes duplicate rows, and saves the cleaned dataframe to a new file.
"""
import challenge_meli.utils.paths as path
from challenge_meli.utils.meli_utils import check_quality,drop_missing_values
import pandas as pd

from challenge_meli.utils.logger import get_logging_config

import logging
import logging.config
import warnings

# configurando logging
logging.config.dictConfig(get_logging_config())

# Ignoring warnings
warnings.filterwarnings("ignore")

logging.info('Make Build Featuring Start...')
# Load the data
logging.info('Loading Data...')
data = pd.read_csv(path.data_processed_dir('data_raw.csv'),low_memory=False)

# Remove rows with more than 50% missing values
logging.info('Drop missing values...')
data = drop_missing_values(data, 50)

# Convert the 'date_created' column to a datetime object and extract new features from it
#Cambiamos el formato a fecha
cols_date = ['date_created','last_updated']
for col in cols_date:
    data[col] = pd.to_datetime(data[col], format='%Y-%m-%d %H:%M:%S')

data['Month_created'] = data['date_created'].dt.month_name()
data['day_name_created'] = data['date_created'].dt.day_name()
data['Hour_created'] = data['date_created'].dt.hour
data['Min_created'] = data['date_created'].dt.minute

data['Month_updated']=data['last_updated'].dt.month_name()
data['day_name_updated']=data['last_updated'].dt.day_name()
data['Hour_updated']=data['last_updated'].dt.hour
data['Min_updated']=data['last_updated'].dt.minute

data = data[~data['Month_created'].isin(['March','April','July','June','May','February','January'])]
data = data[~data['Month_updated'].isin(['June','November'])]
# Remove irrelevant columns
drop_cols = ['date_created','last_updated','start_time','stop_time',
            'geolocation_latitude','geolocation_longitude','base_price',
            'initial_quantity','sold_quantity','available_quantity',
            'site_id','international_delivery_mode','seller_address_country.name',
            'seller_address_country.id','seller_address_search_location.state.name',
            'seller_address_search_location.city.name']
data.drop(columns=drop_cols, inplace=True)

# Remove rows with missing values
data.dropna(inplace=True)

# refactor pictures_size
sizes = data['pictures_size'].apply(lambda x: x.split('x'))
data['row_size'] = [item[0] for item in sizes]
data['col_size'] = [item[1] for item in sizes]

sizes = data['pictures_max_size'].apply(lambda x: x.split('x'))
data['row_max_size'] = [item[0] for item in sizes]
data['col_max_size'] = [item[1] for item in sizes]

data = data[data['shipping_mode']!='me1']

# Remove more irrelevant columns
drop_cols = ['seller_id','parent_item_id','category_id','id','pictures_id',
             'seller_address_id','seller_address_search_location.state.id',
             'seller_address_search_location.city.id','seller_address_city.name',
             'seller_address_state.name','seller_address_state.id',
             'thumbnail','secure_thumbnail','permalink','pictures_url',
             'pictures_secure_url','title', 'pictures_size','pictures_max_size']
data.drop(columns=drop_cols, inplace=True)

# Remove duplicate rows
data.drop_duplicates(inplace=True)

cols = ['Hour_created','Min_created','Hour_updated','Min_updated']
data[cols] = data[cols].astype(int)

# Save the cleaned data to a new file
logging.info('create Data...')
data.to_csv(path.data_processed_dir('data_clean.csv'), index=False)

logging.info('Make Build Featuring End...')