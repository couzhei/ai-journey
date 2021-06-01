#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 21:48:14 2020

@author: couzhei
"""
# importing fundamental libraries

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# importing the data

dataset = pd.read_csv("/home/couzhei/Desktop/AI/Machine Learning/Udemy ML/0.Data Preprocessing/Data.csv")
X = dataset.iloc[:,:-1].values
y = dataset.iloc[:,-1].values
#X = dataset.iloc[:,:-1] # if you're into dataframes and series
#y = dataset.iloc[:,-1]

# taking care of missing data

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
imputer.fit(X[:, 1:]) # Remember to exclude all the string columns,
# that's why I started from 1, since the first column is string
X[:, 1:] = imputer.transform(X[:, 1:])

# encoding categorical variables

#   independent variable
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[("encoder", OneHotEncoder(), [0])], remainder="passthrough")
X = np.array(ct.fit_transform(X))

#   dependent variable
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y = le.fit_transform(y)

# splitting the dataset into test set and train set

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

# feature scalling

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train[:, 3:5] = sc.fit_transform(X_train[:, 3:5])
X_test[:, 3:5] = sc.transform(X_test[:, 3:5]) # you don't need to fit it into test set (why?)

