#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 20:53:00 2018

@author: sourabh
"""
import numpy as np
import pandas as pd
import statsmodels.api
from bokeh.plotting import figure, output_file, show



TCS = pd.read_csv('01-04-2015-TO-31-03-2016TCSALLN.csv')
INF = pd.read_csv('01-04-2015-TO-31-03-2016INFYALLN.csv')
Index = pd.read_csv('data.csv')

TCS_I = TCS.merge(Index,how='outer',on='Date')

INF_I = INF.merge(Index,how='outer',on='Date')


 

#3. Color timeseries between two volume shocks in a different color (Red)
cpI = INF_I['Close Price']
cpT = TCS_I['Close Price']

# Calculating the short-window simple moving average
rollingT = cpT.rolling(window=52).mean()
rollingT.head(20)
rollingI = cpI.rolling(window=52).mean()
rollingI.head(20)

#
output_file("volume_stock.html")
start = 51
end = 245
s = figure(title="volume stocks_TCS", x_axis_label='x', y_axis_label='y')
s.line(TCS_I['Close Price'].index,TCS_I['Total Traded Quantity'],color='red', legend="TCS", line_width=2)
s.line(INF_I['Close Price'].index,INF_I['Total Traded Quantity'],color='orange', legend="INFY", line_width=2)

#4. Gradient color in blue spectrum based on difference of 52 week moving average.
w = figure(title="spectrum stocks_TCS", x_axis_label='x', y_axis_label='y')
w.line(rollingT.iloc[start:end].index , rollingT.iloc[start:end] , color='yellow', legend="TCS", line_width=2)
w.line(rollingI.iloc[start:end].index , rollingI.iloc[start:end] , color='green', legend="INF", line_width=2)
show(w)


#Part 1:
#1. Create 4,16,....,52 week moving average(closing price) for each stock and index. This should happen through a function.
def MA(series,week):
    rollingT = series.rolling(window=week).mean()
    #rollingT.head(20)
    return(rollingT)
print(' moving average(closing price) for each stock 52 week',MA(cpT,52))
print(' moving average(closing price) for each stock 4 week',MA(cpT,4))


#3. Create the following dummy time series:
#3.1 Volume shocks - If volume traded is 10% higher/lower than previous day - make a 0/1 boolean time series for shock, 0/1 dummy-coded time series for direction of shock.
def V_S(data):
    t = data['Total Traded Quantity']
    d = np.diff(data['Total Traded Quantity'])
    volume_shocks = []      ###volume_shocks list
    for i in range(len(d)):
        if(d[i]>0.1*t[i]):
            volume_shocks.append(0)
        elif(d[i]<0.1*t[i]):
            volume_shocks.append(1)
    #print(volume_shocks)
    return(volume_shocks)

#3.2 Price shocks - If closing price at T vs T+1 has a difference > 2%, then 0/1 boolean time series for shock, 0/1 dummy-coded time series for direction of shock.
def P_S(data):
    tt = data['Close Price']
    dd = np.diff(data['Close Price'])
    price_shocks = []      ###volume_shocks list
    for i in range(len(dd)):
        if(dd[i]>0.02*tt[i]):
            price_shocks.append(0)
        elif(dd[i]<0.02*tt[i]):
            price_shocks.append(1)   
    #print(price_shocks)
    return(price_shocks)

print('volume shock dummy time series  on TCS data',V_S(TCS_I))
print('price shock dummy time series on TCS data',P_S(TCS_I))

print('volume shock dummy time series  on INFosys data',V_S(INF_I))
print('price shock dummy time series on INFosys data',P_S(INF_I))




price_shocks_INF = V_S(INF_I)
volume_shocks_INF =  P_S(INF_I)

price_shocks_TCS = V_S(TCS_I)
volume_shocks_TCS =  P_S(TCS_I)


#pd.DataFrame([price_shocks,volume_shocks])
P_V_INF = []
for i in range(len(price_shocks_INF)):
    if price_shocks_INF[i]==0 and volume_shocks_INF[i]==1:
        #print(i)
        P_V_INF.append(1)
    else:
        P_V_INF.append(0)
        
#3.4 Pricing shock without volume shock - based on points a & b - Make a 0/1 dummy time series.
print('Pricing shock without volume shock for INFOSYS data',P_V_INF)

#------------------------------------------------------------------

#Part 2 (data visualization ):
#1. Create timeseries plot of close prices of stocks/indices with the following features:
#2. Color timeseries in simple blue color.
output_file("close_price.html")
p = figure(title="close prices of stocks", x_axis_label='x', y_axis_label='y')
p.line(np.arange(len(TCS_I['Close Price'])),TCS_I['Close Price'],color='blue', legend="TCS", line_width=2)
p.line(np.arange(len(INF_I['Close Price'])),INF_I['Close Price'],color='blue', legend="INFY", line_width=2)




inn = np.where(pd.DataFrame(volume_shocks_INF)==0)[0]
ss = INF_I.iloc[inn,8]
p.line(ss.index,ss,color='red', legend="shocks_INFY", line_width=4,line_dash = "4 4")

tss = np.where(pd.DataFrame(volume_shocks_TCS)==0)[0]
tvs = TCS_I.iloc[tss,8]
p.line(tvs.index,tvs,color='red', legend="shocks_TCS", line_width=4,line_dash = "4 4")

show(p)