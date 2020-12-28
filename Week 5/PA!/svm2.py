# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 07:23:38 2020

@author: Parshva Timbadia
"""


#IMPORTING LIBRARIES

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

#IMPORT DATASET.
colnames = ['Class', 'cap-shape', 'cap-surface','cap-color', 'bruises',
            'odor', 'gill-attachment', 'gill-spacing','gill-size', 'gill-color',
                'stalk-shape', 'stalk-root', 'stalk-surface-above-ring', 
                    'stalk-surface-below-ring','stalk-color-above-ring',
                        'stalk-color-below-ring' , 'veil-type', 'veil-color',
                        'ring-number', 'ring-type', 'spore-print-color',
                        'population', 'habitat']
dataset= pd.read_csv("agaricus-lepiota.data", names = colnames)


# print(dataset.head())
# print(len(dataset))

#Replacing ? to NaN 
dataset=dataset.replace(['?'], np.nan)

#Checking for the NULL values in the dataset.
check_for_null =dataset.isnull().sum()
# print(check_for_null)

#After printinh we were able to see that there were missing values. 

dataset[colnames] =dataset[colnames].fillna(dataset.mode().iloc[0])

# check_for_null =dataset.isnull().sum()
# print(check_for_null)
#We can see that the missing values get handled.

# creating instance of labelencoder
labelencoder = LabelEncoder()
for i in colnames:
    dataset[i]=labelencoder.fit_transform(dataset[i])
#Spliting dependent and Independent variables

# print(dataset.head())
x= dataset.iloc[:, 1:].values
y= dataset.iloc[:, 0].values

#Now we will seperate Training Data and Testing Data. Note: Random State helps to collect Dataset randomly for testing data.
x_train, x_test , y_train , y_test = train_test_split(x, y, test_size=0.2)


#Now using SVC object to train the data.
"""

NOTE: If you want accuracy to be more accurate like 1.0 for this dataset. Make the following changes in 
the SVC model. 

kernel='poly'
degree=8 

NOTE: As we have not included Randon_State to some value, everytime you run the algorithm, it will 
provide different accuracy as it will select Training and Testing Data randomly. Howver, it always 
touches 0.97 + in linear case.

"""
svc_model=SVC(kernel='linear')
svc_model.fit(x_train, y_train)

#Now making predictions. 

y_pred = svc_model.predict(x_test)

#Testing Accuracy Now.

print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred))
print("Model Score :", svc_model.score(x_test, y_test))



