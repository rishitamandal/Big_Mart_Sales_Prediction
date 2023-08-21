# -*- coding: utf-8 -*-
"""SalePrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W_XoX6naZ-1rn1PXJOn_wgBxGVmj-_zZ

Importing The Dependencies
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics

"""Data Collection & Analysis"""

# loading the dataset from csv file to a Pandas Dataframe.
big_mart_data = pd.read_csv('/content/Train.csv')

#first 5 rows of the dataframe
#head() will specify the row if not mentioned than default it will show 5 rows
big_mart_data.head()

#first 10 rows of the dataframe
big_mart_data.head(10)

# number of data points(row) & number of features(column)
#shape gives number of rows and column
big_mart_data.shape

# getting some information about the dataset
#info() will give all information regarding dataset
big_mart_data.info()

"""Categorical Features: (Object)

*   Item_Identifier
*   Item_Fat_Content
*   Item_Type
*   Outlet_Identifier
*   Outlet_Size
*   Outlet_Location_Type
*   Outlet_Type
"""

# checking for missing values
big_mart_data.isnull().sum()

"""Handling Missing Values


> Mean --> Average value (for number)


> Mode --> Most repeated value (for object)




"""

# mean value of "Item_Weight" column
big_mart_data['Item_Weight'].mean()

# filling the missing values in "Item weight" column with "Mean" value
# filling nun values in column with its mean value not using other's column value
big_mart_data['Item_Weight'].fillna(big_mart_data['Item_Weight'].mean(), inplace = True)
# Optional, default False. If True: the replacing is done on the current DataFrame. If False: returns a copy where the replacing is done.

big_mart_data.isnull().sum()

"""Replacing the missing values in "Outlet_size" with mode"""

# mode of "Outlet_Size" column
big_mart_data['Outlet_Size'].mode()

# filling the missing values in "Outlet_Size" column with Mode
mode_of_Outlet_size = big_mart_data.pivot_table(values='Outlet_Size', columns='Outlet_Type', aggfunc=(lambda x: x.mode()[0]))
#lambda is like def function but it is used only once but def can be used many time;

print(mode_of_Outlet_size)

miss_values = big_mart_data['Outlet_Size'].isnull()

print(miss_values)

# replacing missing values in outlet_size
big_mart_data.loc[miss_values, 'Outlet_Size'] = big_mart_data.loc[miss_values,'Outlet_Type'].apply(lambda x: mode_of_Outlet_size[x])

big_mart_data.isnull().sum()
#checking missing values

"""Data Analysis"""

# stastical measure about the data
big_mart_data.describe()

"""Numerical Features"""

# gives theme
sns.set()

#Item_Weight distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_Weight'])
plt.show()

#Item_Visibility distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_Visibility'])

#Item_MRP distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_MRP'])

#Outlet_Establishment_Year distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Outlet_Establishment_Year'])

#	Item_Outlet_Sales distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_Outlet_Sales'])

# Outlet_Establishment_Year column
plt.figure(figsize=(6,6))
sns.countplot(x='Outlet_Establishment_Year',data=big_mart_data)
plt.show()

"""Categorical Features:
*   Item_Fat_Content
*   Item_Type
*   Outlet_Size
*   Outlet_Location_Type
*   Outlet_Type
"""

# Item_Fat_Content column
plt.figure(figsize=(6,6))
sns.countplot(x='Item_Fat_Content',data=big_mart_data)
plt.show()

# Item_Type column
#(6,6)=(x-axis,y-axis) inc or dec as per required.
plt.figure(figsize=(30,6))
sns.countplot(x='Item_Type',data=big_mart_data)
plt.show()

big_mart_data['Outlet_Size'].value_counts()

# Outlet_Size column
plt.figure(figsize=(6,6))
sns.countplot(x='Outlet_Size', data=big_mart_data)
plt.show()
#not working

# Outlet_Location_Type column
plt.figure(figsize=(6,6))
sns.countplot(x='Outlet_Location_Type',data=big_mart_data)
plt.title('Item')
plt.show()

# Outlet_Type column
plt.figure(figsize=(10,6))
sns.countplot(x='Outlet_Type',data=big_mart_data)
plt.show()

"""Data Pre-Processing"""

big_mart_data.head()

# value_counts() function returns object containing counts of unique values
big_mart_data['Item_Fat_Content'].value_counts()

# changing names
big_mart_data.replace({'Item_Fat_Content':{'low fat':'Low Fat', 'LF':'Low Fat', 'reg':'Regular'}}, inplace=True)

big_mart_data['Item_Fat_Content'].value_counts()

"""Label Encoding"""

encoder = LabelEncoder()

big_mart_data['Item_Identifier'] = encoder.fit_transform(big_mart_data['Item_Identifier'])
big_mart_data['Item_Fat_Content'] = encoder.fit_transform(big_mart_data['Item_Fat_Content'])
big_mart_data['Item_Type'] = encoder.fit_transform(big_mart_data['Item_Type'])
big_mart_data['Outlet_Identifier'] = encoder.fit_transform(big_mart_data['Outlet_Identifier'])
big_mart_data['Outlet_Size'] = encoder.fit_transform(big_mart_data['Outlet_Size'])
big_mart_data['Outlet_Location_Type'] = encoder.fit_transform(big_mart_data['Outlet_Location_Type'])
big_mart_data['Outlet_Type'] = encoder.fit_transform(big_mart_data['Outlet_Type'])

big_mart_data.head()

"""Splitting Features and Target"""

# axis = 1 (column), axis=0 (row)
# x shows entire dataset expect deleted columns
# y shows entire column got deleted
X = big_mart_data.drop(columns='Item_Outlet_Sales', axis=1)
Y = big_mart_data['Item_Outlet_Sales']

print(X)

print(Y)

"""Splitting the data into Training_Data & Testing_Data"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

print(X.shape, X_train.shape, X_test.shape)

"""Machine Learning Model Training

XGBoost Regressor
"""

regressor = XGBRegressor()

regressor.fit(X_train, Y_train)

"""Evaluation"""

# prediction on training data
training_data_prediction = regressor.predict(X_train)

# R squared Value
r2_train = metrics.r2_score(Y_train, training_data_prediction)

print('R Squared Value = ', r2_train)

# prediction on training data
test_data_prediction = regressor.predict(X_test)

r2_test = metrics.r2_score(Y_test, test_data_prediction)

print('R Squared Value = ', r2_test)