#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 01:46:53 2021

Class: CS 677 - 

Homework 3


@author: xiang ji
"""

import os
import pandas as pd
import numpy as np
import statistics
from sklearn.model_selection import train_test_split
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier

from sklearn.linear_model import LogisticRegression

from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


data='BankNote_Authentication'

input_dir = r'/Users/estherji/Desktop/jjixiang_hw_3/'
ticker_file = os.path.join(input_dir, data + '.csv')



try:  
    with open(ticker_file) as f:
        lines = f.read().splitlines()
        df = pd.read_csv( 'BankNote_Authentication.csv')
        print('opened file for data: ', data)
    """    your code for assignment 3 goes here
    """
    #Q1(1)
    df['color'] = np.where(df['class'] > 0, 'red', 'green')        
    df.to_csv('myData.csv')#write csv   
    df0 = df[df['class'] == 0]
    df1 = df[df['class'] == 1]
    #Q1(2)
    def colmeanstd (col,datafr):     
        f1 = datafr[col]
    
        f1std = statistics.stdev(f1)
    
        f1mean = statistics.mean(f1)
        print("the mean of", col , "is :", f1mean)
        print("the std of", col , "is :", f1std)
        return
    
    #all
    colmeanstd('variance', df)
    colmeanstd('skewness', df)
    colmeanstd('curtosis', df)
    colmeanstd('entropy', df)
    #0

    colmeanstd('variance', df0)        
    colmeanstd('skewness', df0)
    colmeanstd('curtosis', df0)
    colmeanstd('entropy', df0)    
    #1

    colmeanstd('variance', df1)        
    colmeanstd('skewness', df1)
    colmeanstd('curtosis', df1)
    colmeanstd('entropy', df1)     
    #Q1(3)
    
    #Q2(1)
    #print("df0", df0)
    #split your dataset X into training Xtrain and Xtesting parts (50/50 split)
    
    #for class = 0
    X = df0[["variance","skewness","curtosis","entropy"]]
    y = df0["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
    #scaler
    X = MinMaxScaler().fit_transform(X)      

    
         #Using ”pairplot”
    pair_plot = sns.pairplot(X_train[['variance','skewness','curtosis','entropy']])
    plt.savefig('good_bills.pdf')
    #for class = 1
    X = df1[["variance","skewness","curtosis","entropy"]]
    y = df1["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
        
    
    #scaler
    X = MinMaxScaler().fit_transform(X)  
    pair_plot2 = sns.pairplot(X_train[['variance','skewness','curtosis','entropy']])
    plt.savefig('fake_bills.pdf')    
 
    #Q2(2)
   # df['color'] = np.where(df['class'] > 0, 'red', 'green')      
    df['Mylabel'] = np.where((df['variance'] < -3) & (df['skewness'] < -3) & (df['curtosis'] > 8), 'fake', 'good')

    df.to_csv('myData.csv')#write csv      

    #Q2(4)       
    X = df[["variance","skewness","curtosis","entropy", "Mylabel"]]
    y = df["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
    
    ind = X_test.index.values
    ind = list(ind)
   # print(ind)
   # print("b", y_test[5] == 0)
    #print("aa",X_test['Mylabel'][5]== 'good' )

    
    #tp
    tp = 0
        
    for i in ind:    
        if(X_test['Mylabel'][i]== 'good') and (y_test[i]== 0):
            tp = tp +1
    print("the number of tp of my Label", tp)    
    
    #fp
    fp = 0
    for i in ind:    
        if(X_test['Mylabel'][i]== 'good') and y_test[i]== 1:
            fp = fp +1
    print("the number of fp of my Label", fp)    
    
    #tn
    tn = 0        
    for i in ind:    
        if(X_test['Mylabel'][i]== 'fake') and y_test[i]== 1:
            tn = tn +1
    print("the number of tn of my Label", tn)  

    #fn
    fn = 0        
    for i in ind:    
        if(X_test['Mylabel'][i]== 'fake') and y_test[i]== 0:
            fn = fn +1
    print("the number of fn of my Label", fn) 
    
    
    print("The TPR for mylable ", tp/(tp+fn))
    print("The TNR for mylable ", tn/(tn+fp))    
    print("The Accuracy for mylable ", (tp+tn)/(tp+fp+fn+tn))
    #(TP+TN)/(TP+FP+FN+TN)
    

  #Q3(1)  

   #take k = 3,5,7,9,11.
   #k= 3
    X = df[["variance","skewness","curtosis","entropy"]]
    y = df["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
    #scaler
    X = MinMaxScaler().fit_transform(X)  
   
    def knnacctest (n):
       knn = KNeighborsClassifier(n_neighbors=n)
       knn.fit(X_train, y_train)
       # Predict on dataset which model has not seen before
       knn.predict(X_test) 
       # Calculate the accuracy of the model
       acc = knn.score(X_test, y_test)
       return acc



    
    neighbors = [3,5,7,9,11]
    
     #Q3(2)plot a graph

    # Generate plot   
    ylist=np.array([])
    for i in neighbors:
        #knnacc (i)
        print("The accuracy of k = ",i,"is", knnacctest(i))
        ylist = np.append(ylist, knnacctest(i))
    #print(ylist)
    plt.plot(neighbors,ylist, label = 'Training dataset Accuracy')
    
    plt.legend()
    plt.xlabel('neighbors')
    plt.ylabel('Accuracy')
    plt.show()          
    #plt.savefig('kacc.pdf') 
  #3. use the optimal value k∗ = 3
   # print(len(df0))
    #762
    #print(len(df1))
    #610

    #BUID
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
    new_instance = np.asmatrix([6,8,3,7])
    prediction = knn.predict(new_instance)
    print("BUID for knn = 3", prediction)
    #BUID [1]
   
#Question 4
        #dropf1
        #split your dataset X into training Xtrain and Xtesting parts (50/50 split)
    X = df[["skewness","curtosis","entropy"]]
    y = df["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
    #scaler
    X = MinMaxScaler().fit_transform(X)         
    
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
       # Predict on dataset which model has not seen before
    knn.predict(X_test) 
       # Calculate the accuracy of the model
    acc = knn.score(X_test, y_test)
   
    print("accuracy for drop f1 :", acc)

        #dropf2
        #split your dataset X into training Xtrain and Xtesting parts (50/50 split)
    X = df[["variance","curtosis","entropy"]]
    y = df["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
    #scaler
    X = MinMaxScaler().fit_transform(X)         
    
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
       # Predict on dataset which model has not seen before
    knn.predict(X_test) 
       # Calculate the accuracy of the model
    acc = knn.score(X_test, y_test)
   
    print("accuracy for drop f2 :", acc)
    
        #dropf3
        #split your dataset X into training Xtrain and Xtesting parts (50/50 split)
    X = df[["variance","skewness","entropy"]]
    y = df["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
    #scaler
    X = MinMaxScaler().fit_transform(X)         
    
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
       # Predict on dataset which model has not seen before
    knn.predict(X_test) 
       # Calculate the accuracy of the model
    acc = knn.score(X_test, y_test)
   
    print("accuracy for drop f3 :", acc)    
    
    #dropf4
    X = df[["variance","skewness","curtosis"]]
    y = df["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
    #scaler
    X = MinMaxScaler().fit_transform(X)         
    
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
       # Predict on dataset which model has not seen before
    knn.predict(X_test) 
       # Calculate the accuracy of the model
    acc = knn.score(X_test, y_test)
   
    print("accuracy for drop f4 :", acc) 
    
    #Q5(1)
    #split your dataset X into training Xtrain and Xtesting parts (50/50 split)
    X = df[["variance","skewness","curtosis","entropy"]]
    y = df["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
    #scaler
    
    X = MinMaxScaler().fit_transform(X)  

    lgm = LogisticRegression(solver='liblinear',random_state=1)

    lgm.fit(X_train, y_train)
    
    predictions = lgm.predict(X_test)
    score = lgm.score(X_test, y_test)
    print("The accuracy for LG X_test: ", score)
    
    #Q5(2)
    cm5 = metrics.confusion_matrix(y_test, predictions)
    print(cm5)
    
    
    print("The TPR for LG ", 374/(374+7))
    print("The TNR for LG ", 305/(305+0))  
    
    
    #BUID
       

    new_x = (np.asmatrix([6,8,3,7]))
    new_x = MinMaxScaler().fit_transform(new_x) 
    predicted = lgm.predict(new_x)
    print("LG BUID", prediction)
    #LG BUID [1]
    #Q6(1)
        #dropf1
        #split your dataset X into training Xtrain and Xtesting parts (50/50 split)
    X = df[["skewness","curtosis","entropy"]]
    y = df["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
    #scaler
    X = MinMaxScaler().fit_transform(X)         
    lgm = LogisticRegression(solver='liblinear',random_state=1)

    lgm.fit(X_train, y_train)
    
    predictions = lgm.predict(X_test)
    score = lgm.score(X_test, y_test)
    print("The accuracy for X_test(drop f1): ", score)
 
 #dropf2
        #split your dataset X into training Xtrain and Xtesting parts (50/50 split)
    X = df[["variance","curtosis","entropy"]]
    y = df["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
    #scaler
    X = MinMaxScaler().fit_transform(X)        
    lgm = LogisticRegression(solver='liblinear',random_state=1)

    lgm.fit(X_train, y_train)
    
    predictions = lgm.predict(X_test)
    score = lgm.score(X_test, y_test)
    print("The accuracy for X_test(drop f2): ", score)    

        #dropf3
        #split your dataset X into training Xtrain and Xtesting parts (50/50 split)
    X = df[["variance","skewness","entropy"]]
    y = df["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
    #scaler
    X = MinMaxScaler().fit_transform(X)    
    lgm = LogisticRegression(solver='liblinear',random_state=1)

    lgm.fit(X_train, y_train)
    
    predictions = lgm.predict(X_test)
    score = lgm.score(X_test, y_test)
    print("The accuracy for X_test(drop f3): ", score)   
    
    #dropf4
    X = df[["variance","skewness","curtosis"]]
    y = df["class"]  
    X_train,X_test,y_train,y_test=\
        train_test_split(X, y, train_size=0.5, stratify=y)
    #scaler
    X = MinMaxScaler().fit_transform(X)       
    lgm = LogisticRegression(solver='liblinear',random_state=1)

    lgm.fit(X_train, y_train)
    
    predictions = lgm.predict(X_test)
    score = lgm.score(X_test, y_test)
    print("The accuracy for X_test(drop f4): ", score)      
except Exception as e:
    print(e)
    print('failed to read  data: ', data)



