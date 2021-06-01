#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 02:47:53 2020

@author: couzhei
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data"
    
df = pd.read_csv(url, header=None)
# header=None indicates that the dataframe doesn't include a header row
# thus don't interpret the first row as the header
header = "symboling normalized-losses make fuel-type" + \
    " aspiration num-of-doors body-style drive-wheels" +\
        " engine-location wheel-base length width height"+\
            " curb-weight engine-type num-of-cylinders"+\
                " engine-size fuel-system bore stroke"+\
                    " compression-ratio horsepower peak-rpm"+\
                        " city-mpg highway-mpg price"


header = header.split()

# To label the first row as a natural sheet
df.columns = header

# some useful info
print(df.info)
# Checking the types
print(df.dtypes)
# Checking descriptive statistics
print(df.describe(include="all")) # include = "all" includes the cate data as well

# Missing values on the dependent part! :(
df.dropna(subset=["price"], axis=0, inplace=True)
# didn't work! shit!
# How about?
# df1 = df[df["price"] != "?"]
# Or
# df["price"] = df["price"].replace({'?': np.nan}).astype(float)
# and now!
# df.dropna(subset=["price"], axis=0, inplace=True)
# You may want to save your progress of the Data Cleaning process
# on a new .csv file. In order to do that we use to_csv() method
# =============================================================================
# replace "?" to NaN
df.replace("?", np.nan, inplace = True)
df.head(5)
# df["price"].dropna( axis = 0, inplace = True) # wrong! it takes a series
df.dropna(subset = ["price"], axis = 0, inplace = True)

# reset index, because we droped some rows
df.reset_index(drop=True, inplace=True)

# Other data cleaning using pandas
df["normalized-losses"].replace(np.nan,
                                df["normalized-losses"]
                                .astype("float")
                                .mean(axis=0),
                                inplace=True)

df["bore"].replace(np.nan, df['bore']
                   .astype('float').mean(axis=0), inplace=True)

df["stroke"].replace(np.nan, df["stroke"]
                     .astype(np.float).mean(axis = 0), inplace=True)

df['horsepower'].replace(np.nan, df['horsepower']
                         .astype('float').mean(axis=0), inplace=True)

df['peak-rpm'].replace(np.nan, df['peak-rpm']
                       .astype('float').mean(axis=0), inplace=True)

# Oops some num-of-doors are missing
# Since 84% of sedans are four doors we will go for replacing with foor
df['num-of-doors'].value_counts()
# Or the max
df['num-of-doors'].value_counts().idxmax()
#replace the missing 'num-of-doors' values by the most frequent 
df["num-of-doors"].replace(np.nan, "four", inplace=True)

# The last step in data cleaning is checking and making sure that all 
# data is in the correct format (int, float, text or other).
df.dtypes

df[["bore", "stroke"]] = df[["bore", "stroke"]].astype("float")
df[["normalized-losses"]] = df[["normalized-losses"]].astype("int")
df[["price"]] = df[["price"]].astype("float")
df[["peak-rpm"]] = df[["peak-rpm"]].astype("float")

df.dtypes

# Convert mpg to L/100km by mathematical operation (235 divided by mpg)
df['city-mpg'] = 235/df["city-mpg"]

# Renaming it, so that people can understand its unit
df.rename(columns={"city-mpg": "city-L/100km"}, inplace=True)

# Same goes for highway-mpg
df["highway-mpg"] = 235/df["highway-mpg"]
df.rename(columns={"highway-mpg": "highway-L/100km"}, inplace=True)

# Oh, and about horsepower and peak, I want to convert them into floats
# but to avoid any possible error let's check if there's any nan there!
(df["horsepower"] != np.nan).value_counts() 
(df["peak-rpm"] != np.nan).value_counts()
# Both looks fine

# Btw, np.nan is float T.T
type(np.nan)

df[["horsepower", "peak-rpm"]] = df[["horsepower", "peak-rpm"]].astype(np.float)

# Turbo nad fuel type
dummy_variable_1 = pd.get_dummies(df["aspiration"], prefix="aspiration", prefix_sep="-")
dummy_variable_2 = pd.get_dummies(df["fuel-type"], prefix="fuel-type", prefix_sep="-")
df = pd.concat([df, dummy_variable_1, dummy_variable_2], axis=1)
# Let's get rid of fuel-type and aspiration columns
df.drop(["fuel-type", "aspiration"], axis =1, inplace=True)

# Since I'm using spyder, I alwyas want to make my Variable explorer tab clean
del dummy_variable_1, dummy_variable_2
# Finally save our results
path = "~/Desktop/Data Science/Data Analysis/automobile.csv"
df.to_csv(path)
# =============================================================================
# The above method .dropna() didn't work until I used one of the followings 
# which I don't remember atm
# df1 = df
# df1 = df[not (df["price"] == "?")]
# df["price"].replace({'?': np.nan}).dropna().astype(float)
# =============================================================================
# 
# =============================================================================


# importing the data
X = df.iloc[:, :-1]
y = df.iloc[:,-1]