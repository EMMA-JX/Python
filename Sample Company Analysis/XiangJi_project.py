#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 01:41:10 2021

Instructions how to run this code:
1.	Click run
2.	Enter a s&p500 company stock code(Example: AAPL, MSFT, NVDA, KO, INTC, TETR)

This program can query the asset liability ratio of all companies in the s&p500.
 After calculating the asset liability ratio, 
 the program will help the user to determine if the company is a company 
 with a high level of debt and save the results of each query in a text file.

@author: estherji
"""

#pip install yfinance
#pip install pandas_datareader

import yfinance as yf
from pandas_datareader import data
import pandas as pd
import re

#greeting class
class sayhello:
    "This is a  class"
    

    def greet(self):
        print('Hello')
call = sayhello()
call.greet()

#query start
print("you have 3 times to check a company's asset liability ratio")

#count for 3 query times
for i in range(3): 
  print("---")  
  print("hello, You are using the No.", i+1, "free checking opportunity")

  


  MSFT = input("Enter a stock code: ")

  msft = yf.Ticker(MSFT)
# get stock info

#msft.balance_sheet

  balancesheet = pd.DataFrame(msft.balance_sheet)

  t_a = balancesheet.loc['Total Assets',:]




  def totalasst(x,y):
        temp = balancesheet.loc[x,:]
        temp[y]
        return temp[y]

  ta_2020 = totalasst('Total Assets',0)

#print(ta_2020)
#######################

  Long_debt = balancesheet.loc['Long Term Debt',:]

  def longdebt(x,y):
        temp = balancesheet.loc[x,:]
        temp[y]
        return temp[y]

  ld_2020 = longdebt('Long Term Debt',0)
    
 
#print(totalasst())
#print(ld_2020)
########################
  short_debt = balancesheet.loc['Short Long Term Debt',:]

  def shortdebt(x,y):
    temp = balancesheet.loc[x,:]
    temp[y]
    return temp[y]

  sd_2020 = shortdebt('Short Long Term Debt',0)
#print(sd_2020)

  def totaldebt(x,y):
    tdt = x+y
    return tdt

  td_2020 = totaldebt(ld_2020,sd_2020)
#print(totaldebt(ld_2020,sd_2020))
    
    
#asset_liability_ratio

  def alr(x,y):
    r = x/y
    return r
  alrtest = alr(td_2020,ta_2020)

  if alrtest > 0.6:
    print("This company have too much debt.")
  else:
    print("This company has a good Asset liability ratio:",alrtest, "you can check the txt file for exact number.")
    
    f = open("stock_alr.txt", "w")


    print("The asset lability ratio is: ", alr(td_2020,ta_2020), file=f)


    f.close()
    
    
    
  
else:
    print("Sorry, you have used up all three free inquiries")  
    
