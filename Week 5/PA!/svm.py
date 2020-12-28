# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 16:04:53 2020

@author: Parshva Timbadia
"""

# We are asked to create the SVM for two datasets ie, Iris and Mushroom 

#We will first implement the IRIS. 

#IMPORTING LIBRARIES

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix





#IMPORT DATASET.
colnames = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']
dataset= pd.read_csv("iris.data", names = colnames)
#Seperating the features and the result.

# print(dataset.head())

x= dataset.iloc[:, :-1].values
y= dataset.iloc[:, -1].values

#Checking for the NULL values in the dataset.
check_for_null =dataset.isnull().sum()
# print(check_for_null)
#Now as we dont have any null values we can proceed further with Encoding the Dependent Variable.

#Now we will seperate Training Data and Testing Data. 
'''
Note: Random_State helps to split Training and Testing in a specific manner.

You may include Random_State=0 in the given below line to get accuracy 1.0.
'''
x_train, x_test , y_train , y_test = train_test_split(x, y, test_size=0.2)

# print(len(x_train))
# print(len(x_test))


#Now using SVC object to train the data.

svc_model=SVC(kernel='linear')
svc_model.fit(x_train, y_train)

#Now making predictions. 

y_pred = svc_model.predict(x_test)

#Testing Accuracy Now.

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
print("Model Score :", svc_model.score(x_test, y_test))





