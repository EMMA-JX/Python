#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 05:48:57 2021

@author: estherji
"""
import os
import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score



data='heart_failure_clinical_records_dataset'

input_dir = r'/Users/estherji/Desktop/jjixiang_hw4_677/'
ticker_file = os.path.join(input_dir, data + '.csv')


def sse (act, pred): 
    diff = pred - act
    abs_diff = np.absolute(diff)
    summ = sum(abs_diff)
    square = summ*summ
    return square

try:  
    with open(ticker_file) as f:
        lines = f.read().splitlines()
        df = pd.read_csv( 'heart_failure_clinical_records_dataset.csv')
        print('opened file for data: ', data)
    """    your code for assignment 4 goes here
    """

    
    #Q1(1)load the data into Pandas dataframe. Extract two dataframes
#with the above 4 features: df_0 for surviving patients (DEATH EVENT = 0) 
#and df_1 for deceased patients (DEATH EVENT = 1)
    df_0 = df[df['DEATH_EVENT'] == 0]
    df_1 = df[df['DEATH_EVENT'] == 1]
    
    df_1 = df_1[['creatinine_phosphokinase', 'serum_creatinine', 'serum_sodium', 'platelets']]  
    df_0 = df_0[['creatinine_phosphokinase', 'serum_creatinine', 'serum_sodium', 'platelets']]  
    #print(df_0, df_1)
    # for df_1
    corrMatrix_1 = df_1.corr()
    df_1plot = sn.heatmap(corrMatrix_1, annot=True)
    plt.savefig('corrMatrix_1.pdf') 
    plt.show()
    
    #print(corrMatrix_1)    
     #for df_0
    corrMatrix_0 = df_0.corr()
    df_0plot = sn.heatmap(corrMatrix_0, annot=True)
    plt.savefig('corrMatrix_0.pdf')     
    plt.show()
   # print(corrMatrix_0)       
    

    #fit the model on Xtrain
    X = df_1["platelets"]
    y = df_1["serum_creatinine"]
    """
    #scaler x
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    #Scaler y
    scaler = StandardScaler()
    scaler.fit(y)
    y = scaler.transform(y)    
    """
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, random_state=3)   
 
     
    degree = 1
    weights = np.polyfit(X_train,y_train, degree)
    model = np.poly1d(weights)     
    print("weights for degree 1, df_1", weights)
    predicted = model(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predicted))
    #print("rmse for degree 1, df_1", rmse)
    r2 = r2_score(y_test, predicted)
    #print("r2 for degree 1, df_1", r2)  
    print("sse for degree 1 ", sse(y_test, predicted))    
   
    
    degree = 2
    weights = np.polyfit(X_train,y_train, degree)
    model = np.poly1d(weights)     
    print("weights for degree 2, df_1", weights)
    predicted = model(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predicted))
    #print("rmse for degree 2, df_1", rmse)
    r2 = r2_score(y_test, predicted)
    #print("r2 for degree 2, df_1", r2)   
    print("sse for degree 2 ", sse(y_test, predicted)) 

    
    degree = 3
    weights = np.polyfit(X_train,y_train, degree)
    model = np.poly1d(weights)     
    print("weights for degree 3, df_1", weights)
    predicted = model(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predicted))
    #print("rmse for degree 3, df_1", rmse)
    r2 = r2_score(y_test, predicted)
    #print("r2 for degree 3, df_1", r2)   
    print("sse for degree 3 ", sse(y_test, predicted))     

    #y = a log (x) + b
    weights = np.polyfit(np.log(X_train), y_train, 1)
    model = np.poly1d(weights)     
    print("weights for y = a log x + b, df_1", weights)
    predicted = model(np.log(X_test))
    rmse = np.sqrt(mean_squared_error(y_test, predicted))
    #print("rmse for y = a log x + b, df_1", rmse)
    r2 = r2_score(y_test, predicted)
    #print("r2 for y = a log x + b, df_1", r2)   
    print("sse for y = a log x + b ", sse(y_test, predicted))    
    
    
    #log y = a log x + b
    weights = np.polyfit(np.log(X_train), np.log(y_train), 1)    
    model = np.poly1d(weights)     
    print("weights for log y = a log x + b, df_1", weights)
    predicted = model(np.log(X_test))
    rmse = np.sqrt(mean_squared_error(np.log(y_test), predicted))
    #print("rmse for log y = a log x + b, df_1", rmse)
    r2 = r2_score(np.log(y_test), predicted)
    #print("r2 for log y = a log x + b, df_1", r2)   
    print("sse for log y = a log x + b ", sse(np.log(y_test), predicted))       
    
##########
#df0

 #fit the model on Xtrain
    X = df_0["platelets"]
    y = df_0["serum_creatinine"]

    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, random_state=3)   
 
     
    degree = 1
    weights = np.polyfit(X_train,y_train, degree)
    model = np.poly1d(weights)     
    print("weights for degree 1, df_0", weights)
    predicted = model(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predicted))
   # print("rmse for degree 1, df_0", rmse)
    r2 = r2_score(y_test, predicted)
    #print("r2 for degree 1, df_0", r2)  
    print("sse for degree 1 , df_0", sse(y_test, predicted))    
   
    
    degree = 2
    weights = np.polyfit(X_train,y_train, degree)
    model = np.poly1d(weights)     
    print("weights for degree 2, df_0", weights)
    predicted = model(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predicted))
    #print("rmse for degree 2, df_0", rmse)
    r2 = r2_score(y_test, predicted)
    #print("r2 for degree 2, df_0", r2)   
    print("sse for degree 2 , df_0", sse(y_test, predicted)) 

    
    degree = 3
    weights = np.polyfit(X_train,y_train, degree)
    model = np.poly1d(weights)     
    print("weights for degree 3, df_0", weights)
    predicted = model(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predicted))
    #print("rmse for degree 3, df_0", rmse)
    r2 = r2_score(y_test, predicted)
    #print("r2 for degree 3, df_0", r2)   
    print("sse for degree 3 ", sse(y_test, predicted))     

    #y = a log (x) + b
    weights = np.polyfit(np.log(X_train), y_train, 1)
    model = np.poly1d(weights)     
    print("weights for y = a log x + b, df_0", weights)
    predicted = model(np.log(X_test))
    rmse = np.sqrt(mean_squared_error(y_test, predicted))
    #print("rmse for y = a log x + b, df_0", rmse)
    r2 = r2_score(y_test, predicted)
    #print("r2 for y = a log x + b, df_0", r2)   
    print("sse for y = a log x + b ", sse(y_test, predicted))    
    
    
    #log y = a log x + b
    weights = np.polyfit(np.log(X_train), np.log(y_train), 1)    
    model = np.poly1d(weights)     
    print("weights for log y = a log x + b, df_0", weights)
    predicted = model(np.log(X_test))
    rmse = np.sqrt(mean_squared_error(np.log(y_test), predicted))
    #print("rmse for log y = a log x + b, df_0", rmse)
    r2 = r2_score(np.log(y_test), predicted)
    #print("r2 for log y = a log x + b, df_0", r2)   
    print("sse for log y = a log x + b， df_0 ", sse(np.log(y_test), predicted))       
    

        

    
    
except Exception as e:
    print(e)
    print('failed to read  data: ', data)
