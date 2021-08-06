#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 02:09:39 2021

@author: estherji

for each of the 5 years, compute the mean and standard deviation for the sets 
R, R− and R+ of daily returns for your stock for each day of the week



"""

import os

ticker='SPY'


input_dir = r'/Users/estherji/Desktop/Ji669_hw1/'
#input_dir = r'/Users/foxzhang/Desktop/111GitHub/Try/Work_python_stock/'
ticker_file = os.path.join(input_dir, ticker + '.csv')

def extract_day_list(local_list,biglist):
    for x in biglist:
        x_list = x.split(",", )
       # print(x_list)
        x_listm1 = x_list[1:len(biglist)]
       # print(x_listm1)
       # print("aaa")
        local_list.append(x_listm1[12])
       # print(x_listm1)
    return local_list

def mean(used_list):
    mean_temp = float(0)
    mean_temp = (sum(used_list))/(len(used_list))
    return mean_temp

def calc_std(float_list, mean_dayr):
    squared_list = [number ** 2 for number in float_list]  
    std = (sum(squared_list))/(len(float_list)) - (mean_dayr **2)
    return std



def sublist(subs,subss,orglist):
    #this is for sublist for any orglists with subs


    
    yearlist = [i for i in orglist if( subs in i) and (subss in i)]  
   
    col_Return = []
    extract_day_list(col_Return,yearlist)

    sublists = list(map(float, col_Return))#this is r float


    return sublists

#will print mean
def weekyearmean(subs,subss,orglist):
    
    Tuesday2015 = sublist(subs, subss, orglist)

    mean_tuesday2015r = mean(Tuesday2015)
    
    return print(subs, subss, "r mean is :", mean_tuesday2015r)  

def weekyearmeanvalue(subs,subss,orglist):#do not print
    
    Tuesday2015 = sublist(subs, subss, orglist)

    mean_tuesday2015r = mean(Tuesday2015)
    
    return mean_tuesday2015r

def neglist(weekday, year, list) :
    Monday2016list = sublist(weekday,year,list)
    pMonday2016 = [num for num in Monday2016list if num < 0] 
    
    return pMonday2016

def poslist(weekday, year, list) :
    Monday2016list = sublist(weekday,year,list)
    pMonday2016 = [num for num in Monday2016list if num >= 0] 
    
    return pMonday2016
 
def posstd (weekday, year, list) :
        Monday2016list = sublist(weekday,year,list)
        pMonday2016 = [num for num in Monday2016list if num >= 0] 
        a = calc_std(pMonday2016, posmeanvalue (weekday, year, list))
        
        return a
    
def negstd (weekday, year, list) :
        Monday2016list = sublist(weekday,year,list)
        pMonday2016 = [num for num in Monday2016list if num < 0] 
        a = calc_std(pMonday2016, negmeanvalue(weekday, year, list))
        
        return a

def posmean (weekday, year, list) :
        
        Monday2016list = sublist(weekday,year,list)
        pMonday2016 = [num for num in Monday2016list if num >= 0] 
        print("r plus", weekday, year," mean:", mean(pMonday2016))        
            
        
        return mean
    
def posmeanvalue (weekday, year, list) :
        
        Monday2016list = sublist(weekday,year,list)
        pMonday2016 = [num for num in Monday2016list if num >= 0] 
        a = mean(pMonday2016)    
            
        
        return a

def negmeanvalue (weekday, year, list) :
        
        Monday2016list = sublist(weekday,year,list)
        NegMonday2016 = [num for num in Monday2016list if num < 0] 
        a = mean(NegMonday2016)       
            
        
        return a
def negmean (weekday, year, list) :
        
        Monday2016list = sublist(weekday,year,list)
        NegMonday2016 = [num for num in Monday2016list if num < 0] 
        print("r minus", weekday, year," mean:", mean(NegMonday2016))        
            
        
        return mean


try:  
    with open(ticker_file) as f:
        lines = f.read().splitlines()
    print('opened file for ticker: ', ticker)
    """    your code for assignment 1 goes here
   
    """

    
    Mondayfulllist = [i for i in lines if( 'Monday' in i) and ('0' in i)] 
    Tuesdayfulllist = [i for i in lines if( 'Tuesday' in i) and ('0' in i)] 
    Wednesdayfulllist = [i for i in lines if( 'Wednesday' in i) and ('0' in i)] 
    Thursdayfulllist = [i for i in lines if( 'Thursday' in i) and ('0' in i)] 
    Fridayfulllist = [i for i in lines if( 'Friday' in i) and ('0' in i)] 
    #question 1 （1）compute the mean and standard deviation for the sets R, R− and R+ of daily returns  
   

    col_Return =[]
    extract_day_list(col_Return,lines)  #outputs col_Return
   
    col_Return.pop(0)
    col_Return_float = list(map(float, col_Return)) #converts strings to float

    #print(col_Return_float)
   # print("Result:")
   # print(sum(col_Return_float))#return list

    mean_r = mean(col_Return_float)
    print("r mean is ", mean_r)
   
    #r mean
   
    #------------------------------Monday
    Monday = sublist('Monday','0', lines)
    mean_mondayr = mean(Monday)    
 
    weekyearmean('Monday','0', lines)
    


    

    #----for 2015 Monday

    weekyearmean('Monday','2015', lines)
    
    #----for 2016 Monday
 
    weekyearmean('Monday','2016', lines)    
    #----for 2017 Monday

    weekyearmean('Monday','2017', lines)
    
    #----for 2018 Monday

    weekyearmean('Monday','2018', lines)
    
    #----for 2019 Monday

    weekyearmean('Monday','2019', lines)
    
    #------------------------------Tuesday
    Tuesday = sublist('Tuesday','0', lines)
    mean_tuesdayr = mean(Tuesday)    

    weekyearmean('Tuesday','0', lines)
    
    
    #---for 2015 tuesday
    
    weekyearmean('Tuesday','2015', lines)
    
    #---for 2016 tuesday
    
    weekyearmean('Tuesday','2016', lines)
        
 
    
    #---for 2017 tuesday
    
    weekyearmean('Tuesday','2017', lines)
    
    
    #---for 2018 tuesday
    
    weekyearmean('Tuesday','2018', lines)

    
    #---for 2019 tuesday
    

    
    
    weekyearmean('Tuesday','2019', lines)
    
    
    
    #------------------------------Wednesday
    
    Wednesday = sublist('Wednesday','0', lines)
    mean_Wednesdayr = mean(Wednesday)    

    weekyearmean('Wednesday','0', lines)
    
    #----for 2015 Wednessday
    weekyearmean('Wednesday','2015', lines)    
    
    #----for 2016 Wednessday
    weekyearmean('Wednesday','2016', lines)    
    
    #----for 2017 Wednessday
    weekyearmean('Wednesday','2017', lines)
        
        
    #----for 2018 Wednessday
    weekyearmean('Wednesday','2018', lines)    
    
    #----for 2019 Wednessday
    weekyearmean('Wednesday','2019', lines)       
    
    #------------------------------Thursday      
    
    Thursday = sublist('Thursday','0', lines)
    mean_Thursdayr = mean(Thursday)    

    weekyearmean('Thursday','0', lines)
    
    #----for 2015 Thursday
    weekyearmean('Thursday','2015', lines)    
    
    #----for 2016 Thursday
    weekyearmean('Thursday','2016', lines)    
    
    #----for 2017 Thursday
    weekyearmean('Thursday','2017', lines)
        
        
    #----for 2018 Thursday
    weekyearmean('Thursday','2018', lines)    
    
    #----for 2019 Thursday
    weekyearmean('Thursday','2019', lines)   
         
    #------------------------------Friday
     

    
    Friday = sublist('Friday','0', lines)
    mean_Fridayr = mean(Friday)    

    weekyearmean('Friday','0', lines)      
 
    #----for 2015 Friday
    weekyearmean('Friday','2015', lines)    
    
    #----for 2016 Friday
    weekyearmean('Friday','2016', lines)    
    
    #----for 2017 Friday
    weekyearmean('Friday','2017', lines)
        
        
    #----for 2018 Friday
    weekyearmean('Friday','2018', lines)    
    
    #----for 2019 Friday
    weekyearmean('Friday','2019', lines) 
   
    
   
    #for r std
    #算list square
    #算/n
   
   
    #this is r square list
    squared_list_r = [number ** 2 for number in col_Return_float ]
    a = sum(squared_list_r)
   
    #std
    std_r = (a/(len(lines)-1)) - (mean_r * mean_r)
    print("r std :", std_r)
   

    #Monday r std
    print("Monday r std is", calc_std(Monday,mean_mondayr))
        
    

    
    #1需要2015 Monday r list

    #2 need 2015 monday mean
    
    print("2015 monday r std is :", calc_std(sublist('Monday','2015',lines), weekyearmeanvalue('Monday','2015', lines) ))
    print("2016 monday r std is :", calc_std(sublist('Monday','2016',lines), weekyearmeanvalue('Monday','2016', lines) ))
    print("2017 monday r std is :", calc_std(sublist('Monday','2017',lines), weekyearmeanvalue('Monday','2017', lines) ))
    print("2018 monday r std is :", calc_std(sublist('Monday','2018',lines), weekyearmeanvalue('Monday','2018', lines) ))
    print("2019 monday r std is :", calc_std(sublist('Monday','2019',lines), weekyearmeanvalue('Monday','2019', lines) ))
   
   
    #Tuesday r std
    print("Tuesday std is", calc_std(Tuesday,mean_tuesdayr))
    
    print("2015 Tuesday r std is :", calc_std(sublist('Tuesday','2015',lines), weekyearmeanvalue('Tuesday','2015', lines) ))
    print("2016 Tuesday r std is :", calc_std(sublist('Tuesday','2016',lines), weekyearmeanvalue('Tuesday','2016', lines) ))
    print("2017 Tuesday r std is :", calc_std(sublist('Tuesday','2017',lines), weekyearmeanvalue('Tuesday','2017', lines) ))
    print("2018 Tuesday r std is :", calc_std(sublist('Tuesday','2018',lines), weekyearmeanvalue('Tuesday','2018', lines) ))
    print("2019 Tuesday r std is :", calc_std(sublist('Tuesday','2019',lines), weekyearmeanvalue('Tuesday','2019', lines) ))
  
   
    #Wednesday r std
    print("Wednesday std is", calc_std(Wednesday,mean_Wednesdayr))
    
    print("2015 Wednesday r std is :", calc_std(sublist('Wednesday','2015',lines), weekyearmeanvalue('Wednesday','2015', lines) ))
    print("2016 Wednesday r std is :", calc_std(sublist('Wednesday','2016',lines), weekyearmeanvalue('Wednesday','2016', lines) ))
    print("2017 Wednesday r std is :", calc_std(sublist('Wednesday','2017',lines), weekyearmeanvalue('Wednesday','2017', lines) ))
    print("2018 Wednesday r std is :", calc_std(sublist('Wednesday','2018',lines), weekyearmeanvalue('Wednesday','2018', lines) ))
    print("2019 Wednesday r std is :", calc_std(sublist('Wednesday','2019',lines), weekyearmeanvalue('Wednesday','2019', lines) ))
  
     

   
    #Thursday r std
    print("Thursday std is", calc_std(Thursday,mean_Thursdayr))  
    
    print("2015 Thursday r std is :", calc_std(sublist('Thursday','2015',lines), weekyearmeanvalue('Thursday','2015', lines) ))
    print("2016 Thursday r std is :", calc_std(sublist('Thursday','2016',lines), weekyearmeanvalue('Thursday','2016', lines) ))
    print("2017 Thursday r std is :", calc_std(sublist('Thursday','2017',lines), weekyearmeanvalue('Thursday','2017', lines) ))
    print("2018 Thursday r std is :", calc_std(sublist('Thursday','2018',lines), weekyearmeanvalue('Thursday','2018', lines) ))
    print("2019 Thursday r std is :", calc_std(sublist('Thursday','2019',lines), weekyearmeanvalue('Thursday','2019', lines) ))
   
    #Friday r std
    print("Friday std is", calc_std(Friday,mean_Fridayr))    
    print("2015 Friday r std is :", calc_std(sublist('Friday','2015',lines), weekyearmeanvalue('Friday','2015', lines) ))
    print("2016 Friday r std is :", calc_std(sublist('Friday','2016',lines), weekyearmeanvalue('Friday','2016', lines) ))
    print("2017 Friday r std is :", calc_std(sublist('Friday','2017',lines), weekyearmeanvalue('Friday','2017', lines) ))
    print("2018 Friday r std is :", calc_std(sublist('Friday','2018',lines), weekyearmeanvalue('Friday','2018', lines) ))
    print("2019 Friday r std is :", calc_std(sublist('Friday','2019',lines), weekyearmeanvalue('Friday','2019', lines) ))
      
   
   
 # ------------------------------------------------------------------------------------------------
   
   
    ######for r+ list
    posir = [num for num in col_Return_float if num >= 0]


   # print("Positive numbers in the list: ", *posir)
   
    mean_rp = mean(posir)
    
    print("r plus mean is ", mean_rp)  
    
    
   
    #std for r plus
    # 1 find sum of rp square list
    squared_list_rp = [number ** 2 for number in posir ]  
   
    b = sum(squared_list_rp)
        #this is r square/n
       
      #r plus std
    std_rp = (b/(len(posir))) - (mean_rp * mean_rp)

   
    print("r plus std :", std_rp)

    #Monday
    pMonday = [num for num in Monday if num >= 0]
    mean_pMonday = mean(pMonday)
    print("r plus Monday mean is ", mean_pMonday)   

    
    # 2015 r plus Monday mean
    Monday2015list = sublist('Monday','2015',Mondayfulllist)
    pMonday2015 = [num for num in Monday2015list if num >= 0] 
    print("r plus Monday 2015 mean:", mean(pMonday2015))


    
    
    # 2016 r plus Monday mean


    posmean('Monday', '2016', Mondayfulllist)
    
    # 2017 r plus Monday mean
    posmean('Monday', '2017', Mondayfulllist) 
    # 2018 r plus Monday mean
    posmean('Monday', '2018', Mondayfulllist)
    # 2019 r plus Monday mean
    posmean('Monday', '2019', Mondayfulllist)
    #def!!!!!!!!!!!!!!!!!!!!!!pos year mean 
    #def!!!!!!!!!!!!!!!!!!!!!!neg year mean
   #def posmeans ()
    
    #Tuesday
    pTuesday = [num for num in Tuesday if num >= 0]
    mean_pTuesday = mean(pTuesday)
    print("r plus Tuesday mean is ", mean_pTuesday) 
    
    # 2015 r plus Tuesday mean
    posmean('Tuesday', '2015', Tuesdayfulllist) 
     # 2016 r plus Tuesday mean
    posmean('Tuesday', '2016', Tuesdayfulllist)
    
    # 2017 r plus Tuesday mean
    posmean('Tuesday', '2017', Tuesdayfulllist) 
    # 2018 r plus Tuesday mean
    posmean('Tuesday', '2018', Tuesdayfulllist)
    # 2019 r plus Tuesday mean
    posmean('Tuesday', '2019', Tuesdayfulllist)
    
    
    #Wednesday
    pWednesday = [num for num in Wednesday if num >= 0]
    mean_pWednesday = mean(pWednesday)
    print("r plus Wednesday mean is ", mean_pWednesday)  
    
    
    # 2015 r plus Wednesday mean
    posmean('Wednesday', '2015', Wednesdayfulllist) 
     # 2016 r plus Wednesday mean
    posmean('Wednesday', '2016', Wednesdayfulllist)
    # 2017 r plus Wednesday mean
    posmean('Wednesday', '2017', Wednesdayfulllist) 
    # 2018 r plus Wednesday mean
    posmean('Wednesday', '2018', Wednesdayfulllist)
    # 2019 r plus Wednesday mean
    posmean('Wednesday', '2019', Wednesdayfulllist)    
    
    
    #Thursday
    pThursday = [num for num in Thursday if num >= 0]
    mean_pThursday = mean(pThursday)
    print("r plus Thursday mean is ", mean_pThursday)  
    
    # 2015 r plus Thursday mean
    posmean('Thursday', '2015', Thursdayfulllist) 
     # 2016 r plus Thursday mean
    posmean('Thursday', '2016', Thursdayfulllist)
    # 2017 r plus Thursday mean
    posmean('Thursday', '2017', Thursdayfulllist) 
    # 2018 r plus Thursday mean
    posmean('Thursday', '2018', Thursdayfulllist)
    # 2019 r plus Thursday mean
    posmean('Thursday', '2019', Thursdayfulllist)



    
    #Friday
    pFriday = [num for num in Friday if num >= 0]
    mean_pFriday = mean(pFriday)
    print("r plus Friday mean is ", mean_pFriday)  
    
    # 2015 r plus Friday mean
    posmean('Friday', '2015', Fridayfulllist) 
    # 2016 r plus Friday mean
    posmean('Friday', '2016', Fridayfulllist)
    # 2017 r plus Friday mean
    posmean('Friday', '2017', Fridayfulllist) 
    # 2018 r plus Friday mean
    posmean('Friday', '2018', Fridayfulllist)
    # 2019 r plus Friday mean
    posmean('Friday', '2019', Fridayfulllist)    
    
    
    
    
   
    #std for r plus
    #Monday r std
    print("Monday std for r plus is", calc_std(pMonday,mean_pMonday))  

    #1 finds 2015 monday r plus list
    
    
    #2 finds mean

    print("2015 monday r plus std is :", posstd('Monday', '2015', lines))
    print("2016 monday r plus std is :", posstd('Monday', '2016', lines))
    print("2017 monday r plus std is :", posstd('Monday', '2017', lines))
    print("2018 monday r plus std is :", posstd('Monday', '2018', lines))
    print("2019 monday r plus std is :", posstd('Monday', '2019', lines))
    #Tuesday r std
    print("Tuesday std for r plus is", calc_std(pTuesday,mean_pTuesday))    
       
    print("2015 Tuesday r plus std is :", posstd('Tuesday', '2015', lines))
    print("2016 Tuesday r plus std is :", posstd('Tuesday', '2016', lines))
    print("2017 Tuesday r plus std is :", posstd('Tuesday', '2017', lines))
    print("2018 Tuesday r plus std is :", posstd('Tuesday', '2018', lines))
    print("2019 Tuesday r plus std is :", posstd('Tuesday', '2019', lines))
    #Wednesday r std
    print("Wednesday std for r plus is", calc_std(pWednesday,mean_pWednesday))    
    
    print("2015 Wednesday r plus std is :", posstd('Wednesday', '2015', lines))
    print("2016 Wednesday r plus std is :", posstd('Wednesday', '2016', lines))
    print("2017 Wednesday r plus std is :", posstd('Wednesday', '2017', lines))
    print("2018 Wednesday r plus std is :", posstd('Wednesday', '2018', lines))
    print("2019 Wednesday r plus std is :", posstd('Wednesday', '2019', lines))
    #Thursday r std
    print("Thursday std for r plus is", calc_std(pThursday,mean_pThursday))    

    print("2015 Thursday r plus std is :", posstd('Thursday', '2015', lines))
    print("2016 Thursday r plus std is :", posstd('Thursday', '2016', lines))
    print("2017 Thursday r plus std is :", posstd('Thursday', '2017', lines))
    print("2018 Thursday r plus std is :", posstd('Thursday', '2018', lines))
    print("2019 Thursday r plus std is :", posstd('Thursday', '2019', lines))         
    #Friday r std
    print("Friday std for r plus is", calc_std(pFriday,mean_pFriday))    
         
    print("2015 Friday r plus std is :", posstd('Friday', '2015', lines))
    print("2016 Friday r plus std is :", posstd('Friday', '2016', lines))
    print("2017 Friday r plus std is :", posstd('Friday', '2017', lines))
    print("2018 Friday r plus std is :", posstd('Friday', '2018', lines))
    print("2019 Friday r plus std is :", posstd('Friday', '2019', lines))     
   
   
    #######
    #for r minus list
    minus_r = [num for num in col_Return_float if num < 0]
   
   # print("Negative numbers in the list: ", *minus_r)
   
    # r minus mean
    mean_rm = (sum(minus_r))/(len(minus_r))#r-mean
    print("r minus mean is ", mean_rm)
    
    

    
   
    #std for r minus
    # 1 find r minus square list
    squared_list_rm = [number ** 2 for number in minus_r ]  
    #r minus list square/n
 
    c = sum(squared_list_rm)
    #r minus std
    std_rm = (c/(len(minus_r))) - (mean_rm * mean_rm)
    print("r minus std :", std_rm)
   
    #Monday
    nMonday = [num for num in Monday if num < 0]
    mean_nMonday = mean(nMonday)
    print("r minus Monday mean is ", mean_nMonday)    
    # 2015 r minus Monday mean
    negmean('Monday', '2015', Mondayfulllist)
    # 2016 r minus Monday mean
    negmean('Monday', '2016', Mondayfulllist)
    # 2017 r minus Monday mean
    negmean('Monday', '2017', Mondayfulllist) 
    # 2018 r minus Monday mean
    negmean('Monday', '2018', Mondayfulllist)
    # 2019 r minus Monday mean
    negmean('Monday', '2019', Mondayfulllist)



    
    #Tuesday
    nTuesday = [num for num in Tuesday if num < 0]
    mean_nTuesday = mean(nTuesday)
    print("r minus Tuesday mean is ", mean_nTuesday)  

    # 2015 r minus Tuesday mean
    negmean('Tuesday', '2015', Tuesdayfulllist) 
     # 2016 r minus Tuesday mean
    negmean('Tuesday', '2016', Tuesdayfulllist)
    
    # 2017 r minus Tuesday mean
    negmean('Tuesday', '2017', Tuesdayfulllist) 
    # 2018 r minus Tuesday mean
    negmean('Tuesday', '2018', Tuesdayfulllist)
    # 2019 r minus Tuesday mean
    negmean('Tuesday', '2019', Tuesdayfulllist)

    
    #Wednesday
    nWednesday = [num for num in Wednesday if num < 0]
    mean_nWednesday = mean(nWednesday)
    print("r minus Wednesday mean is ", mean_nWednesday)  

    # 2015 r minus Wednesday mean
    negmean('Wednesday', '2015', Wednesdayfulllist) 
     # 2016 r minus Wednesday mean
    negmean('Wednesday', '2016', Wednesdayfulllist)
    # 2017 r minus Wednesday mean
    negmean('Wednesday', '2017', Wednesdayfulllist) 
    # 2018 r minus Wednesday mean
    negmean('Wednesday', '2018', Wednesdayfulllist)
    # 2019 r minus Wednesday mean
    negmean('Wednesday', '2019', Wednesdayfulllist)      
    
    
    
    #Thursday
    nThursday = [num for num in Thursday if num < 0]
    mean_nThursday = mean(nThursday)
    print("r minus Thursday mean is ", mean_nThursday)   
    
    # 2015 r minus Thursday mean
    negmean('Thursday', '2015', Thursdayfulllist) 
     # 2016 r minus Thursday mean
    negmean('Thursday', '2016', Thursdayfulllist)
    # 2017 r minus Thursday mean
    negmean('Thursday', '2017', Thursdayfulllist) 
    # 2018 r minus Thursday mean
    negmean('Thursday', '2018', Thursdayfulllist)
    # 2019 r minus Thursday mean
    negmean('Thursday', '2019', Thursdayfulllist)    
    
    
    
    #Friday
    nFriday = [num for num in Friday if num < 0]
    mean_nFriday =mean(nFriday)
    print("r minus Friday mean is ", mean_nFriday)  
    
    # 2015 r minus Friday mean
    negmean('Friday', '2015', Fridayfulllist) 
    # 2016 r minus Friday mean
    negmean('Friday', '2016', Fridayfulllist)
    # 2017 r minus Friday mean
    negmean('Friday', '2017', Fridayfulllist) 
    # 2018 r minus Friday mean
    negmean('Friday', '2018', Fridayfulllist)
    # 2019 r minus Friday mean
    negmean('Friday', '2019', Fridayfulllist)    
    
        
   

    #std for r minus
    #Monday r std
    print("Monday std for r minus is", calc_std(nMonday,mean_nMonday))   
    
    print("2015 monday r minus std is :", negstd('Monday', '2015', lines))
    print("2016 monday r minus std is :", negstd('Monday', '2016', lines))
    print("2017 monday r minus std is :", negstd('Monday', '2017', lines))
    print("2018 monday r minus std is :", negstd('Monday', '2018', lines))
    print("2019 monday r minus std is :", negstd('Monday', '2019', lines))
    
   
    #Tuesday r std
    print("Tuesday std for r minus is", calc_std(nTuesday,mean_nTuesday))    

    print("2015 Tuesday r minus std is :", negstd('Tuesday', '2015', lines))
    print("2016 Tuesday r minus std is :", negstd('Tuesday', '2016', lines))
    print("2017 Tuesday r minus std is :", negstd('Tuesday', '2017', lines))
    print("2018 Tuesday r minus std is :", negstd('Tuesday', '2018', lines))
    print("2019 Tuesday r minus std is :", negstd('Tuesday', '2019', lines))
    
       
    #Wednesday r std
    print("Wednesday std for r minus is", calc_std(nWednesday,mean_nWednesday))    

    print("2015 Wednesday r minus std is :", negstd('Wednesday', '2015', lines))
    print("2016 Wednesday r minus std is :", negstd('Wednesday', '2016', lines))
    print("2017 Wednesday r minus std is :", negstd('Wednesday', '2017', lines))
    print("2018 Wednesday r minus std is :", negstd('Wednesday', '2018', lines))
    print("2019 Wednesday r minus std is :", negstd('Wednesday', '2019', lines))
    
         
    #Thursday r std
    print("Thursday std for r minus is", calc_std(nThursday,mean_nThursday))    

    print("2015 Thursday r minus std is :", negstd('Thursday', '2015', lines))
    print("2016 Thursday r minus std is :", negstd('Thursday', '2016', lines))
    print("2017 Thursday r minus std is :", negstd('Thursday', '2017', lines))
    print("2018 Thursday r minus std is :", negstd('Thursday', '2018', lines))
    print("2019 Thursday r minus std is :", negstd('Thursday', '2019', lines))
   
       
    #Friday r std
    print("Friday std for r minus is", calc_std(nFriday,mean_nFriday))   
    
    
    print("2015 Friday r minus std is :", negstd('Friday', '2015', lines))
    print("2016 Friday r minus std is :", negstd('Friday', '2016', lines))
    print("2017 Friday r minus std is :", negstd('Friday', '2017', lines))
    print("2018 Friday r minus std is :", negstd('Friday', '2018', lines))
    print("2019 Friday r minus std is :", negstd('Friday', '2019', lines))
   
    
    

    print("number of minus day on monday", len(nMonday))
    print("number of minus day on Tuesday", len(nTuesday))
    print("number of minus day on Wednesday", len(nWednesday))
    print("number of minus day on Thursday", len(nThursday))
    print("number of minus day on Friday", len(nFriday))    


    print("number of minus day on monday 2015", len(neglist('Monday', '2015', lines)))
    print("number of minus day on monday 2016", len(neglist('Monday', '2016', lines)))
    print("number of minus day on monday 2017", len(neglist('Monday', '2017', lines)))    
    print("number of minus day on monday 2018", len(neglist('Monday', '2018', lines)))
    print("number of minus day on monday 2019", len(neglist('Monday', '2019', lines)))
    

    print("number of minus day on Tuesday 2015", len(neglist('Tuesday', '2015', lines)))
    print("number of minus day on Tuesday 2016", len(neglist('Tuesday', '2016', lines)))
    print("number of minus day on Tuesday 2017", len(neglist('Tuesday', '2017', lines)))    
    print("number of minus day on Tuesday 2018", len(neglist('Tuesday', '2018', lines)))
    print("number of minus day on Tuesday 2019", len(neglist('Tuesday', '2019', lines)))
    

    print("number of minus day on Wednesday 2015", len(neglist('Wednesday', '2015', lines)))
    print("number of minus day on Wednesday 2016", len(neglist('Wednesday', '2016', lines)))
    print("number of minus day on Wednesday 2017", len(neglist('Wednesday', '2017', lines)))    
    print("number of minus day on Wednesday 2018", len(neglist('Wednesday', '2018', lines)))
    print("number of minus day on Wednesday 2019", len(neglist('Wednesday', '2019', lines)))
    

    print("number of minus day on Thursday 2015", len(neglist('Thursday', '2015', lines)))
    print("number of minus day on Thursday 2016", len(neglist('Thursday', '2016', lines)))
    print("number of minus day on Thursday 2017", len(neglist('Thursday', '2017', lines)))    
    print("number of minus day on Thursday 2018", len(neglist('Thursday', '2018', lines)))
    print("number of minus day on Thursday 2019", len(neglist('Thursday', '2019', lines)))
 

    print("number of minus day on Friday 2015", len(neglist('Friday', '2015', lines)))
    print("number of minus day on Friday 2016", len(neglist('Friday', '2016', lines)))
    print("number of minus day on Friday 2017", len(neglist('Friday', '2017', lines)))    
    print("number of minus day on Friday 2018", len(neglist('Friday', '2018', lines)))
    print("number of minus day on Friday 2019", len(neglist('Friday', '2019', lines)))
    
       
       
   
    
   

    print("number of plus day on Monday", len(pMonday))
    print("number of plus day on Tuesday", len(pTuesday))
    print("number of plus day on Wednesday", len(pWednesday))
    print("number of plus day on Thursday", len(pThursday))
    print("number of plus day on Friday", len(pFriday))    
    
    poslist
    print("number of plus day on monday 2015", len(poslist('Monday', '2015', lines)))
    print("number of plus day on monday 2016", len(poslist('Monday', '2016', lines)))
    print("number of plus day on monday 2017", len(poslist('Monday', '2017', lines)))    
    print("number of plus day on monday 2018", len(poslist('Monday', '2018', lines)))
    print("number of plus day on monday 2019", len(poslist('Monday', '2019', lines)))
    

    print("number of plus day on Tuesday 2015", len(poslist('Tuesday', '2015', lines)))
    print("number of plus day on Tuesday 2016", len(poslist('Tuesday', '2016', lines)))
    print("number of plus day on Tuesday 2017", len(poslist('Tuesday', '2017', lines)))    
    print("number of plus day on Tuesday 2018", len(poslist('Tuesday', '2018', lines)))
    print("number of plus day on Tuesday 2019", len(poslist('Tuesday', '2019', lines)))
    

    print("number of plus day on Wednesday 2015", len(poslist('Wednesday', '2015', lines)))
    print("number of plus day on Wednesday 2016", len(poslist('Wednesday', '2016', lines)))
    print("number of plus day on Wednesday 2017", len(poslist('Wednesday', '2017', lines)))    
    print("number of plus day on Wednesday 2018", len(poslist('Wednesday', '2018', lines)))
    print("number of plus day on Wednesday 2019", len(poslist('Wednesday', '2019', lines)))
    

    print("number of plus day on Thursday 2015", len(poslist('Thursday', '2015', lines)))
    print("number of plus day on Thursday 2016", len(poslist('Thursday', '2016', lines)))
    print("number of plus day on Thursday 2017", len(poslist('Thursday', '2017', lines)))    
    print("number of plus day on Thursday 2018", len(poslist('Thursday', '2018', lines)))
    print("number of plus day on Thursday 2019", len(poslist('Thursday', '2019', lines)))
 

    print("number of plus day on Friday 2015", len(poslist('Friday', '2015', lines)))
    print("number of plus day on Friday 2016", len(poslist('Friday', '2016', lines)))
    print("number of plus day on Friday 2017", len(poslist('Friday', '2017', lines)))    
    print("number of plus day on Friday 2018", len(poslist('Friday', '2018', lines)))
    print("number of plus day on Friday 2019", len(poslist('Friday', '2019', lines)))
    
       
           
    

   
    #question 1 （2）
    #question 1 （3）
    print("number of plus day", len(poslist('0', '0', lines)))
    print("number of minus day", len(neglist('0', '0', lines)))
    
       
    
    
    #question 1 （4）  
    #does your stock lose more on a ”down” day than it gains on an ”up” days.
    #sum of r plus
    rlist = sublist('0','0',lines)
    rplus = [num for num in rlist if num >= 0] 
    

    print("the sum of rplus is", sum(rplus))
    
    

    rmin = [num for num in rlist if num < 0] 
    print("the sum of r minus is", sum(rmin))
       
    
    
    
    
    #question 1 （5）
   
    #question 2 （1）
    #question 2 （2）
    #question 2 （3）
    #question 2 （4）
   
    #question 3 （1）
    #question 3 （2）
   
    #question 4 （1）
    #You listen to the oracle and follow its advice. How much much money will you have on the last trading day of 2019:
        #my stock
    rplus_new = [x+1 for x in rplus]        
    moneyiwillhave = 100
    
    for i in range(len(rplus)):
        
        moneyiwillhave = rplus_new[i]*moneyiwillhave
 
    print("Money I will have for JPM with listen to oracle is ", moneyiwillhave)
    #print("Money I will have for SPY with listen to oracle is ", moneyiwillhave)    

        

   
    #question 5 （1）
    #for JPM
    rlist_plusone = [x+1 for x in rlist]  
    
    beginmoney = 100
    
    for i in range(len(rplus)):
        
        beginmoney = rlist_plusone[i]*beginmoney
        

    print("Money I will have for SPY with buy and hold is ", beginmoney)
    
    
    #Money I will have for SPY with buy and hold is  128.12844238819153
    #Money I will have for JPM with buy and hold is  160.73549128519383

    #question 5 （2）
   
    #question 6 （a）
    #since I missed the best 10 days 
    sorted_rplus = sorted(rplus_new, reverse=True);
    #print("sorted", sorted_rplus )
    del sorted_rplus[0:10]
    #print("sorteddd", sorted_rplus)    
    
    topten = list(set(rplus_new) - set(sorted_rplus))
    question6alist = list(set(rplus_new) - set(topten))
    #print("remove top10list :", question6alist)
    
    beginmoney = 100
    
    for i in range(len(question6alist)):
        
        beginmoney = question6alist[i]*beginmoney
        

    #print("Money I will have for SPY with 6 a is ", beginmoney)   
    print("Money I will have for JPM with 6 a is ", beginmoney)   
    
    
    #question 6 （b）
    
    rmin_new = [1+x for x in rmin] #new means +1
    sorted_rminus = sorted(rmin_new);
    top10minr = sorted_rminus[0:10]
    
    total_rmin_minustop10 = list(set(rmin_new) - set(top10minr))
    
    question6blist = list(set(rlist_plusone) - set(total_rmin_minustop10))
    
    beginmoney = 100
    
    for i in range(len(question6blist)):
        
        beginmoney = question6blist[i]*beginmoney
        

    #print("Money I will have for SPY with 6 b is ", beginmoney)   
    print("Money I will have for JPM with 6 b is ", beginmoney)   
    #Money I will have for SPY with 6 b is  3588.31480888253
    #Money I will have for JPM with 6 b is  36625.01044479383
    
    
    
    
    #question 6 （c）
    #top 5 best
    sortedd_rplus = sorted(rplus_new, reverse=True);
    #print("sorted", sorted_rplus )
    del sorted_rplus[0:5]
    #print("sorteddd", sorted_rplus)    
    
    topfive = list(set(rplus_new) - set(sorted_rplus))

    topworse5 = sorted_rminus[0:5]    
    
    total_rmin_minustop5 = list(set(rmin_new) - set(topworse5))    
    
    

    question6clist = list(set(rlist_plusone) - set(topfive) - set(total_rmin_minustop5))   

    beginmoney = 100
    
    for i in range(len(question6clist)):
        
        beginmoney = question6clist[i]*beginmoney
        

    print("Money I will have for SPY with 6 c is ", beginmoney)   
    #print("Money I will have for JPM with 6 c is ", beginmoney) 
    #Money I will have for JPM with 6 c is  23649.781480541453
    #Money I will have for SPY with 6 c is  2826.3043564872964
   
except Exception as e:
    print(e)
    print('failed to read stock data for ticker: ', ticker)


#print("?")
#print(ticker_file)
#print(ticker)
#print(lines)


