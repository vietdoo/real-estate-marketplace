#System
import sys
import time
import random

#Extract Transform Load
import requests
import pymongo
import json
from bson.json_util import dumps
from bson.json_util import loads
import numpy as np
import pandas as pd

#Visualization
import seaborn as sns
import matplotlib.pyplot as plt

#Machine Learning
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression  
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, confusion_matrix, accuracy_score, r2_score

from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler ,PolynomialFeatures, minmax_scale, MaxAbsScaler ,LabelEncoder, MinMaxScaler

from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor

from sklearn.svm import SVR

#maps
import folium
from folium.plugins import HeatMap


f = open('houses.json')
data = json.load(f)
df = pd.DataFrame(data)
df_del_list = ['account_name', 'ad_id', 'date', 'account_oid', 'videos', 'company_ad', 'owner', 'living_size',
               'pty_jupiter', 'contain_videos', 'number_of_images', 'avatar', 'params', '_id', 'furnishing_sell',
               'phone_hidden', 'escrow_can_deposit', 'street_name', 'zero_deposit', 'region', 'region_name',
               'property_legal_document', 'special_display_images', 'special_display', 'protection_entitlement',
               'property_road_condition', 'property_back_condition', 'apartment_type', 'property_status', 'type',
               'direction', 'detail_address', 'body', 'apartment_feature', 'land_feature', 'reviewer_image',
                'landed_type', 'condition_ad', 'condition_ad_name', 'shop', 'balconydirection', 'projectimages',
               'street_id', 'block', 'project_oid', 'projectid', 'unitnumber_display', 'unitnumber', 
               'streetnumber_display', 'address', 'webp_image', 'has_video', 'shop_alias', 'street_number',
               'land_type', 'size_unit', 'commercial_type', 'floornumber', 'house_type',
               'region_v2', 'area_v2', 'ward', 'location', 'account_id',  'floors',
               'toilets', 'price_string', 'list_time', 'label_campaigns', 'ad_labels']

df.drop(df_del_list, axis = 1, inplace = True, errors = 'ignore')
df = df.dropna() 
df.isnull().sum()

X = df[['longitude', 'latitude']]
clf = IsolationForest(max_samples = 4, random_state = 0)
clf.fit(X)
prediction = clf.fit_predict(X)
print("Number of outliers detected: {}".format((prediction < 0).sum()))

df = df[prediction > 0]
print(df.shape)

new = df.groupby('area_name')

dist_group = []
num_of_outliers = 0
for x, y in new:
    df_new = y
    item = y[['longitude', 'latitude']]
    clf = IsolationForest(max_samples = 4, random_state = 0)
    clf.fit(item)
    prediction = clf.fit_predict(item)
    print("Number of outliers detected in {}: {}".format(df_new.iloc[0]['area_name'], (prediction < 0).sum()))
    num_of_outliers += sum(prediction < 0)
    df_new = df_new[prediction > 0]
    dist_group.append(df_new)
    
print('Total number of outliers:', num_of_outliers)
pd.concat(dist_group).shape

df = pd.concat(dist_group)

randlng = np.random.rand(len(df)) / 10000
randlat = np.random.rand(len(df)) / 10000
dup = df.duplicated(['longitude', 'latitude'])

df['longitude'] = dup * randlng + df['longitude'] 
df['latitude']  = dup * randlat + df['latitude'] 

df = df.drop_duplicates(['longitude', 'latitude'])
df = df[pd.notnull(df['image'])]

clean = df.to_dict(orient = 'records')

def add_link_key(item):
    area_str = ''
    list_id_str = ''
    try:
        area_str = item['area_name'].replace(" ", "-")
        list_id_str = str(item['list_id'])
    except:
        pass
 
    url = 'https://www.nhatot.com/mua-ban-nha-dat-{area}-tp-ho-chi-minh/{list_id}.htm'
    item['url'] = url.format(area = area_str, list_id = list_id_str)


for item in clean:
    add_link_key(item)


with open('clean.json', 'w') as f:
    json.dump(clean, f)