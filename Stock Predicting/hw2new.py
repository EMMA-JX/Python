#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 15:11:42 2021


Class: CS 677 - 

Homework 2


@author: ji xiang
"""



import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#ticker='SPY'
ticker='JPM'



input_dir = r'/Users/estherji/Desktop/677_assignment2/'
#input_dir = r'/Users/foxzhang/Desktop/111GitHub/Try/Work_python_stock/'
ticker_file = os.path.join(input_dir, ticker + '.csv')




try:  
    with open(ticker_file) as f:
        lines = f.read().splitlines()
    print('opened file for ticker: ', ticker)
    """    your code for assignment 1 goes here
   
    """
    #Is all the code for my assignment written here?
    #Q1(1)
    #df = pd.read_csv( 'SPY.csv')
    df = pd.read_csv( 'JPM.csv')
    #print(df)
    #df.to_csv('myDataFrame.csv')#write csv
    df['True Label'] = np.where(df['Return'] >= 0, '+', '-')
    #print(df.head())
    #df.to_csv('myDataFrame.csv')#write csv
    
    plus_days = df[df['True Label'] == '+']
    minus_days = df[df['True Label'] == '-']
    
    #data frame true label
    
    DFT = df['True Label']

    #Q1(2)
    #year1,2 3
    
    L2015 = df[df['Year'] == 2015]
    L2016 = df[df['Year'] == 2016]
    L2017 = df[df['Year'] == 2017]
    L = pd.concat([L2015,L2016,L2017])
    print("lenth of L", len(L))
    
    Lminus = L[L['True Label'] == '-']

    Lplus = L[L['True Label'] == '+']
    
    #year 4,5
    L2018 = df[df['Year'] == 2018]
    L2019 = df[df['Year'] == 2019]
    LT = pd.concat([L2018,L2019])
    #print("lenth of LT", len(LT))
        
    
    LTminus = LT[LT['True Label'] == '-']

    LTplus = LT[LT['True Label'] == '+']
    
    #the Probability that next day is up day
    Pup = (len(Lplus))/(len(L))
    print("The probability that next is UP day is: ", Pup)
    
    #Q1(3)
    
    #K=1
    #1 find k =1 days, 
    #2 then , find exact k=1day
    #3 find exact+1 day
    # if exact+1day is -, - count +1
    # if exact + 1day is +, + count +1
    #-count + +count = totalcount
    #p+ = +count/total count
    #p- = -count/total count
   
    df_ltruelabel = L['True Label']
    #print("length of df_ltruelabel", len(df_ltruelabel))
    #print(df_ltruelabel[1])
    
    
    #k=1
    k1minuscount = 0
    k1pluscount = 0
        
    
    for  x in range(len(df_ltruelabel)-1):
        if  ((df_ltruelabel[x] == '-') and (df_ltruelabel[x+1] == '-')) :
            k1minuscount = k1minuscount +1
        
            
        elif ((df_ltruelabel[x] == '-') and (df_ltruelabel[x+1] == '+')) :
            k1pluscount = k1pluscount+1
            

    
    #print("k = 1 minus count is :", k1minuscount)
    #print("k = 1 plus count is ", k1pluscount)
    print("for k= 1, the probability of '-' then '+'is", (k1pluscount/(k1pluscount+k1minuscount)))
            
        #k=2
    k2minuscount = 0
    k2pluscount = 0
        
    
    for  x in range(len(df_ltruelabel)-1):
        if  (df_ltruelabel[x] == '-') and (df_ltruelabel[x+1] == '-') and (df_ltruelabel[x+2] == '-'):
            k2minuscount = k2minuscount +1
        
            
        elif ((df_ltruelabel[x] == '-') and (df_ltruelabel[x+1] == '-')) and (df_ltruelabel[x+2] == '+') :
            k2pluscount = k2pluscount+1
            

    
    #print("k = 2 minus count is :", k2minuscount)
    #print("k = 2 plus count is ", k2pluscount)
    print("for k= 2, the probability of '-' '-' then '+'is", (k2pluscount/(k2pluscount+k2minuscount)))        
            #k=3
    k3minuscount = 0
    k3pluscount = 0
        
    
    for  x in range(len(df_ltruelabel)-1):
        if  (df_ltruelabel[x] == '-') and (df_ltruelabel[x+1] == '-') and (df_ltruelabel[x+2] == '-') and (df_ltruelabel[x+3] == '-'):
            k3minuscount = k3minuscount +1
        
            
        elif ((df_ltruelabel[x] == '-') and (df_ltruelabel[x+1] == '-')) and (df_ltruelabel[x+2] == '-') and (df_ltruelabel[x+3] == '+'):
            k3pluscount = k3pluscount+1
            

    
    #print("k = 3 minus count is :", k3minuscount)
    #print("k = 3 plus count is ", k3pluscount)
    print("for k= 3, the probability of '-' '-' '-'then '+'is", (k3pluscount/(k3pluscount+k3minuscount)))
    
    
    #Q1(4)
    
    #k=1
    k1minuscount = 0
    k1pluscount = 0
        
    
    for  x in range(len(df_ltruelabel)-1):
        if  ((df_ltruelabel[x] == '+') and (df_ltruelabel[x+1] == '-')) :
            k1minuscount = k1minuscount +1
        
            
        elif ((df_ltruelabel[x] == '+') and (df_ltruelabel[x+1] == '+')) :
            k1pluscount = k1pluscount+1
            

    
    #print("k = 1 minus count is :", k1minuscount)
    #print("k = 1 plus count is ", k1pluscount)
    print("for k= 1, the probability of '+' then '+'is", (k1pluscount/(k1pluscount+k1minuscount)))
            
        #k=2
    k2minuscount = 0
    k2pluscount = 0
        
    
    for  x in range(len(df_ltruelabel)-1):
        if  (df_ltruelabel[x] == '+') and (df_ltruelabel[x+1] == '+') and (df_ltruelabel[x+2] == '-'):
            k2minuscount = k2minuscount +1
        
            
        elif ((df_ltruelabel[x] == '+') and (df_ltruelabel[x+1] == '+')) and (df_ltruelabel[x+2] == '+') :
            k2pluscount = k2pluscount+1
            

    
    #print("k = 2 minus count is :", k2minuscount)
    #print("k = 2 plus count is ", k2pluscount)
    print("for k= 2, the probability of '+' '+' then '+'is", (k2pluscount/(k2pluscount+k2minuscount)))        
            #k=3
    k3minuscount = 0
    k3pluscount = 0
        
    
    for  x in range(len(df_ltruelabel)-1):
        if  (df_ltruelabel[x] == '+') and (df_ltruelabel[x+1] == '+') and (df_ltruelabel[x+2] == '+') and (df_ltruelabel[x+3] == '-'):
            k3minuscount = k3minuscount +1
        
            
        elif ((df_ltruelabel[x] == '+') and (df_ltruelabel[x+1] == '+')) and (df_ltruelabel[x+2] == '+') and (df_ltruelabel[x+3] == '+'):
            k3pluscount = k3pluscount+1
            

    
    #print("k = 3 minus count is :", k3minuscount)
    #print("k = 3 plus count is ", k3pluscount)
    print("for k= 3, the probability of '+' '+' '+'then '+'is", (k3pluscount/(k3pluscount+k3minuscount)))
    
    #Q2(1)

    
    df['W2True Label'] = np.where(df['Return'] >= 0, '+', '-')
    df['W2True Label'] = df['W2True Label'].replace(['+'],'-')
    df['W3True Label'] = np.where(df['Return'] >= 0, '+', '-')
    df['W3True Label'] = df['W3True Label'].replace(['+'],'-')
    df['W4True Label'] = np.where(df['Return'] >= 0, '+', '-')
    df['W4True Label'] = df['W4True Label'].replace(['+'],'-')
    #df.to_csv('myDataFrame.csv')#write csv
    
    #w=2

    def w2pattern_in_training_set_probability_compare (a,b):
        
        #k=2
        k2minuscount = 0
        k2pluscount = 0
    
        for  x in range(len(df_ltruelabel)-1):
            if  (DFT[x] == a) and (DFT[x+1] == b) and (DFT[x+2] == '-'):
                k2minuscount = k2minuscount +1
        
            
            elif ((DFT[x] == a) and (DFT[x+1] == b)) and (DFT[x+2] == '+') :
                k2pluscount = k2pluscount+1
            
            #probability = k2pluscount/(k2pluscount+k2minuscount
            
        if k2pluscount >= k2minuscount:
                label =  "+"
        else:
                label = "-"

        return label

    
    testrange = range(756, 1257)
    for  x in range(756, 1256): 
        a = DFT[x-2]

        b = DFT[x-1]
        value = w2pattern_in_training_set_probability_compare(a,b)
        df.loc[x,'W2True Label'] = value        
        #df.to_csv('myDataFrame.csv')
        #print(w2pattern_in_training_set_probability_compare(DFT[x],DFT[x+1]))
                

    #w=3

    def w3pattern_in_training_set_probability_compare (a,b,c):
        
        #k=2
        k2minuscount = 0
        k2pluscount = 0
    
        for  x in range(len(df_ltruelabel)-1):
            if  (DFT[x] == a) and (DFT[x+1] == b) and (DFT[x+2] == c)and (DFT[x+3] == '-'):
                k2minuscount = k2minuscount +1
        
            
            elif ((DFT[x] == a) and (DFT[x+1] == b)) and DFT[x+2] == c and (DFT[x+3] == '+') :
                k2pluscount = k2pluscount+1
            
            #probability = k2pluscount/(k2pluscount+k2minuscount
            
        if k2pluscount >= k2minuscount:
                label =  "+"
        else:
                label = "-"

        return label

    
    testrange = range(756, 1257)
    for  x in range(756, 1257): 
        a = DFT[x-2]
        c = DFT[x-3]
        b = DFT[x-1]
        value = w3pattern_in_training_set_probability_compare(a,b,c)
        df.loc[x,'W3True Label'] = value        
        #df.to_csv('myDataFrame.csv')
        #print(w2pattern_in_training_set_probability_compare(DFT[x],DFT[x+1]))
                
    
     #w=4

    def w4pattern_in_training_set_probability_compare (a,b,c,d):
        
        #k=2
        k2minuscount = 0
        k2pluscount = 0
    
        for  x in range(len(df_ltruelabel)-1):
            if  (DFT[x] == a) and (DFT[x+1] == b) and (DFT[x+2] == c) and (DFT[x+3] == d) and (DFT[x+4] == '-'):
                k2minuscount = k2minuscount +1
        
            
            elif ((DFT[x] == a) and (DFT[x+1] == b)) and DFT[x+2] == c and (DFT[x+3] == d)and (DFT[x+4] == '+') :
                k2pluscount = k2pluscount+1
            
            #probability = k2pluscount/(k2pluscount+k2minuscount
            
        if k2pluscount >= k2minuscount:
                label =  "+"
        else:
                label = "-"

        return label

    
    #testrange = range(755, 1259)
    for  x in range(755, 1258): 
        a = DFT[x-2]
        c = DFT[x-3]
        b = DFT[x-1]
        d = DFT[x-4]
        value = w4pattern_in_training_set_probability_compare(a,b,c,d)
        df.loc[x,'W4True Label'] = value        
        #df.to_csv('myDataFrame.csv')
        #print(w2pattern_in_training_set_probability_compare(DFT[x],DFT[x+1]))
                
    
    
    #df.to_csv('myDataFrame.csv')
 
        
    
        
        
      

        
    #Q2(2)
    #w= 2
        #year 4,5

   
    number_of_t_plus = len(LTplus)
    number_of_t_minus = len(LTminus)
    #print(len(LT))
    

    
    def number_of_correctplus (comparedcol):
        
        correctplus = 0
        correctminus = 0
        
        
        for i in range(755, 1258):    
            if(df['True Label'][i]==df[comparedcol][i]) and df['True Label'][i]== '+':
                correctplus = correctplus +1
            elif(df['True Label'][i]==df[comparedcol][i]) and df['True Label'][i]== '-':
                correctminus = correctminus +1     
        return correctplus
    
    
    
    def number_of_correctminus (comparedcol):
        
        correctplus = 0
        correctminus = 0
        
        
        for i in range(755, 1258):    
            if(df['True Label'][i]==df[comparedcol][i]) and df['True Label'][i]== '+':
                correctplus = correctplus +1
            elif(df['True Label'][i]==df[comparedcol][i]) and df['True Label'][i]== '-':
                correctminus = correctminus +1     
        return correctminus
    
    #w=2
    w2p = number_of_correctplus('W2True Label')/number_of_t_plus
    w2m = number_of_correctminus('W2True Label')/number_of_t_minus
    print("the accuracy for w2 plus is",w2p )
    print("the accuracy for w2 minus is",w2m )    
    #w=3
    w3p = number_of_correctplus('W3True Label')/number_of_t_plus
    w3m = number_of_correctminus('W3True Label')/number_of_t_minus
    print("the accuracy for w3 plus is",w3p )
    print("the accuracy for w3 minus is",w3m )    
    #w=4
    w4p = number_of_correctplus('W4True Label')/number_of_t_plus
    w4m = number_of_correctminus('W4True Label')/number_of_t_minus
    
    print("the accuracy for w4 plus is", w4p )
    print("the accuracy for w4 minus is",w4m )    
 
        #Q2(3)
    print("total accuracy for w2", w2p+w2m)
    print("total accuracy for w3", w3p+w3m)
    print("total accuracy for w4", w4p+w4m)
    #w3 is highest accuracy for S&P-500
    
    #Q3(1)
    df['ensemble labels'] = np.where(df['Return'] >= 0, '+', '-')
    df['ensemble labels'] = df['ensemble labels'].replace(['+'],'-')
    

    for  i in range(755, 1258): 
        pluscount = 0
        minuscount = 0
        if(df['W2True Label'][i]== '+'):
            pluscount = pluscount +1
        else:
            minuscount = minuscount +1
        if(df['W3True Label'][i]== '+'):
            pluscount = pluscount +1
        else:
            minuscount = minuscount +1        
        if(df['W4True Label'][i]== '+'):
            pluscount = pluscount +1
        else:
            minuscount = minuscount +1   
        if ( pluscount>minuscount ):
            valuee = '+'
            df.loc[i,'ensemble labels'] = valuee
        else:
            valuee = '-'
            df.loc[i,'ensemble labels'] = valuee

    #df.to_csv('myDataFrame.csv')

    
     #Q3(2)   
    #w=2
    elp = number_of_correctplus('ensemble labels')/number_of_t_plus
    elm = number_of_correctminus('ensemble labels')/number_of_t_minus
    print("the accuracy for ensemble labels plus is",elp )
    print("the accuracy for ensemble labels minus is",elm )      
    
    #Q3(3)
    #For plus label, w2 is highest
    
    #Q3(4)
    #for minus label, w4 is highest
    
    #Question 4(1)
    
    #tp
    def tp (col):
        
        correctplus = 0
        
        
        
        for i in range(755, 1258):    
            if(df['True Label'][i]==df[col][i]) and df['True Label'][i]== '+':
                correctplus = correctplus +1
               
        return correctplus
    print("the number of tp of W2True Label", tp('W2True Label'))
    print("the number of tp of W3True Label", tp('W3True Label'))
    print("the number of tp of W4True Label", tp('W4True Label'))
    print("the number of tp of ensemble labels", tp('ensemble labels'))
    
    #fp
    def fp (col):
        count = 0
        
        
        
        for i in range(755, 1258):    
            if (df[col][i]== '+') and df['True Label'][i]== '-':
                count = count +1
               
        return count        
    
    print("the number of fp of W2True Label", fp('W2True Label'))
    print("the number of fp of W3True Label", fp('W3True Label'))
    print("the number of fp of W4True Label", fp('W4True Label'))
    print("the number of fp of ensemble labels", fp('ensemble labels'))    


    #tn
    def tn (col):
        count = 0
        
        
        
        for i in range(755, 1258):    
            if (df[col][i]== '-') and df['True Label'][i]== '-':
                count = count +1
               
        return count         
    print("the number of tn of W2True Label", tn('W2True Label'))
    print("the number of tn of W3True Label", tn('W3True Label'))
    print("the number of tn of W4True Label", tn('W4True Label'))
    print("the number of tn of ensemble labels", tn('ensemble labels'))    


    #fn
    def fn (col):
        count = 0
        
        
        
        for i in range(755, 1258):    
            if (df[col][i]== '-') and df['True Label'][i]== '+':
                count = count +1
               
        return count 
    print("the number of fn of W2True Label", fn('W2True Label'))
    print("the number of fn of W3True Label", fn('W3True Label'))
    print("the number of fn of W4True Label", fn('W4True Label'))
    print("the number of fn of ensemble labels", fn('ensemble labels'))  
    
    
    #tpr
    def tpr(col):
        tprate = tp(col)/(tp(col)+fn(col))
        return tprate
    
    print("the tpr of W2True Label", tpr('W2True Label'))
    print("the tpr of W3True Label", tpr('W3True Label'))
    print("the tpr of W4True Label", tpr('W4True Label'))
    print("the tpr of ensemble labels", tpr('ensemble labels'))  
    
    #tnr
    def tnr(col):
        tnrate = tn(col)/(tn(col)+fp(col))
        return tnrate
    
    print("the tnr of W2True Label", tnr('W2True Label'))
    print("the tnr of W3True Label", tnr('W3True Label'))
    print("the tnr of W4True Label", tnr('W4True Label'))
    print("the tnr of ensemble labels", tnr('ensemble labels'))     
    
    #Accuracy = (TP+TN)/(TP+FP+FN+TN)
    def accuracy(col):
        accrate = (tn(col)+tn(col))/((tn(col)+fp(col)+tp(col)+fn(col)))
        return accrate

    
    print("the accuracy of W2True Label", accuracy('W2True Label'))
    print("the accuracy of W3True Label", accuracy('W3True Label'))
    print("the accuracy of W4True Label", accuracy('W4True Label'))
    print("the accuracy of ensemble labels", accuracy('ensemble labels'))     
    
    
     #Q5   
        
    df['W4growth'] = np.where(df['Return'] >= 0, '+', '-')
    df['W4growth'] = df['W4True Label'].replace(['+'],'-')
    df['ensemble labels growth'] = np.where(df['Return'] >= 0, '+', '-')
    df['ensemble labels growth'] = df['W4True Label'].replace(['+'],'-')
    df['buy and hold'] = np.where(df['Return'] >= 0, '+', '-')
    
    #w = 4
    beginmoney = 100
    
    for i in range(755, 1258):
        
        if df['W4True Label'][i]=='+':

            plusr = df['Return'][i]
            plusr1 = plusr+1
            beginmoney = plusr1*beginmoney
            
            df.loc[i,'W4growth'] = beginmoney
            df.to_csv('myDataFrame.csv')
        else:
            beginmoney = beginmoney
            df.loc[i,'W4growth'] = beginmoney
            df.to_csv('myDataFrame.csv')


 
    
 #ensemble

    
    beginmoney = 100
    
    for i in range(755, 1258):
        
        if df['ensemble labels'][i]=='+':

            plusr = df['Return'][i]
            plusr1 = plusr+1
            beginmoney = plusr1*beginmoney
            
            df.loc[i,'ensemble labels growth'] = beginmoney
            df.to_csv('myDataFrame.csv')
        else:
            beginmoney = beginmoney
            df.loc[i,'ensemble labels growth'] = beginmoney
            df.to_csv('myDataFrame.csv')



  #buy and hold

    beginmoney = 100
    
    for i in range(755, 1258):
        
        beginmoney = (df['Return'][i]+1)*beginmoney
        df.loc[i,'buy and hold'] = beginmoney

        df.to_csv('myDataFrame.csv')  
        
        
    #plot
    df2 = pd.read_csv( 'myDataFrame.csv')
        #year 4,5
    year2018 = df2[df2['Year'] == 2018]
    year2019 = df2[df2['Year'] == 2019]
    
    testset = pd.concat([year2018,year2019])
    
    testset["W4growth"]=testset["W4growth"].astype(float)
    testset["ensemble labels growth"]=testset["ensemble labels growth"].astype(float)
    testset["buy and hold"]=testset["buy and hold"].astype(float)
    
    
    testset.plot(y=["W4growth", "ensemble labels growth", "buy and hold"])
    plt.show()

   
    
  
except Exception as e:
    print(e)
    print('failed to read stock data for ticker: ', ticker)




