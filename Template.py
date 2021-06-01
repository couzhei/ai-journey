#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 04:47:50 2020

@author: couzhei
"""

# importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# importing the dataset
dataset = pd.read_csv(url)
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# Handling the missing data
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
imputer.fit(X[:,1:3]) # change needed! 
X[:,1:3] = imputer.transform(X[:,1:3])

# handling categorical data
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
ct = ColumnTransformer(transformers=[("encoder", OneHotEncoder(),
                                      [0])],
                        remainder="passthrough")
X = np.array(ct.fit_transform(X))
le = LabelEncoder()
y = le.fit_transform(y)


# Splitting the data into test set and training set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling