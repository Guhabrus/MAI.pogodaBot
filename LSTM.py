# -*- coding: utf-8 -*-
"""Копия main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VNUnlIDugdu3MshbDlevXw1lQpjuY2hM
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# импорт данных

df = pd.read_csv('Data.csv')
df['Time'] = pd.to_datetime(df.Time)
df.index = df['Time']
df1 = pd.read_csv('ActData.csv')
df1['Time'] = pd.to_datetime(df1.Time)
df1.index = df1['Time']
df['Direction'] = df.pop('Direction')*np.pi / 180

from sklearn.preprocessing import MinMaxScaler
data = df.sort_index(ascending=True, axis=0)
new_data = pd.DataFrame(index=range(0,len(df)),columns=['Time', 'Ff'])
for i in range(0,len(data)):
    new_data['Time'][i] = data['Time'][i]
    new_data['Ff'][i] = data['Ff'][i]
    
new_data.index = new_data.Time
new_data.drop('Time', axis=1, inplace=True)
dataset = new_data.values


data1 = df1.sort_index(ascending=True, axis=0)
new_data1 = pd.DataFrame(index=range(0,len(df1)),columns=['Time', 'Ff'])
for i in range(0,len(data1)):
    new_data1['Time'][i] = data1['Time'][i]
    new_data1['Ff'][i] = data1['Ff'][i]
    
new_data1.index = new_data1.Time
new_data1.drop('Time', axis=1, inplace=True)
dataset1 = new_data1.values

# скаллируем данные

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)
scaled_data1 = scaler.fit_transform(dataset1)
train= scaled_data[:int(df.shape[0]*0.8)]
valid = scaled_data[int(df.shape[0]*0.8):]
valid1 = scaled_data1[:int(df1.shape[0])]

n_window = 30

x_train,y_train,x_test,y_test, x1_test = [],[],[],[], []
for i in range(n_window,train.shape[0]):
    x_train.append(train[i-n_window:i,0])
    y_train.append(train[i,0])

for z in range(n_window,valid.shape[0]):
    x_test.append(valid[z-n_window:z,0])
    y_test.append(valid[z,0])
for a in range(n_window, valid1.shape[0]):
    x1_test.append(valid1[a-n_window:a,0])

len(x1_test)

x_train, y_train,x_test,y_test = np.array(x_train), np.array(y_train),np.array(x_test),np.array(y_test)
x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

x1_test = np.array(x1_test)

x1_test=np.reshape(x1_test,(x1_test.shape[0],x1_test.shape[1],1))

from keras.models import Sequential
from keras.layers import Dense, Dropout,LSTM
model = Sequential()
model.add(LSTM(units=150,input_shape=(x_train.shape[1],1),return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(100))
model.add(Dropout(0.2))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer="adam")
model.save('model.h5')
model.summary()

history = model.fit(x_train,y_train,validation_data=(x_test,y_test), epochs=15)

plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()

x_test_pred = x1_test[-1].tolist()
for i in range(0,n_window):
  y_pred = model.predict(np.array([x_test_pred]))
  x_test_pred.pop(0)
  x_test_pred.append(y_pred[0])

y_pred = scaler.inverse_transform(x_test_pred)

train= new_data[:int(df1.shape[0]*0.8)]

valid1 = new_data[int(y_pred.shape[0])+n_window:]

plt.plot(y_pred)
plt.savefig('ResultAvgGraphic.png')

# import datetime 
# dstart = datetime.datetime(2021,5,30)
# dnow = datetime.datetime(2021,6,1)
# plt.xlim(dstart, dnow)
# valid1['Predictions'] = y_pred[0]
# plt.xlabel('Date')
# plt.ylabel('Average Wind Speed')
# plt.plot(train['Ff'])
# plt.plot(valid['Ff'])
# line2=plt.plot(valid['Predictions'] )
# import matplotlib.patches as mpatches
# patch=mpatches.Patch(color='green', label='Predicted Average Wind Speed')
# plt.legend(line2,handles=[patch],loc=2,fontsize=10)
# plt.show()

#plt.plot(np.array(valid['Ff']))
#plt.plot(y_pred[0])

import math
from sklearn.metrics import mean_squared_error

#testScore = math.sqrt(mean_squared_error(y_pred[0], np.array(valid['Ff'])))
#print('Test Score: %.2f RMSE' % (testScore))

#print("Avg: %.2f"%np.average(y_pred[0] - np.array(valid['Ff'])))

np.savetxt('wv.csv', (y_pred))

from sklearn.preprocessing import MinMaxScaler
data = df.sort_index(ascending=True, axis=0)
new_data = pd.DataFrame(index=range(0,len(df)),columns=['Time', 'Direction'])
for i in range(0,len(data)):
    new_data['Time'][i] = data['Time'][i]
    new_data['Direction'][i] = data['Direction'][i]
    
new_data.index = new_data.Time
new_data.drop('Time', axis=1, inplace=True)
dataset = new_data.values

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)
train1 = scaled_data[:int(df.shape[0]*0.8)]
valid1 = scaled_data[int(df.shape[0]*0.8):]

x1_train,y1_train,x1_test,y1_test = [],[],[],[]
for i in range(n_window,train1.shape[0]):
    x1_train.append(train1[i-n_window:i,0])
    y1_train.append(train1[i,0])

for z in range(n_window,valid1.shape[0]):
    x1_test.append(valid1[z-n_window:z,0])
    y1_test.append(valid1[z,0])

x1_train, y1_train,x1_test,y1_test = np.array(x1_train), np.array(y1_train),np.array(x1_test),np.array(y1_test)
x1_train = np.reshape(x1_train, (x1_train.shape[0],x1_train.shape[1],1))
x1_test=np.reshape(x1_test,(x1_test.shape[0],x1_test.shape[1],1))

from keras.models import Sequential
from keras.layers import Dense, Dropout,LSTM
model1 = Sequential()
model1.add(LSTM(units=150,input_shape=(x1_train.shape[1],1),return_sequences=True))
model1.add(Dropout(0.2))
model1.add(LSTM(units=50))
model1.add(Dropout(0.2))
model1.add(Dense(100))
model1.add(Dropout(0.2))
model1.add(Dense(1))
model1.compile(loss='mean_squared_error', optimizer="adam")
model1.save('model1.h5')

history1 = model1.fit(x1_train,y1_train,validation_data=(x1_test,y1_test), epochs=15)

plt.plot(history1.history['loss'], label='train')
plt.plot(history1.history['val_loss'], label='test')
plt.legend()
plt.show()

prediction1 = model1.predict(x1_test)
y_pred1 = scaler.inverse_transform(prediction1)
train1 = new_data[:int(df.shape[0]*0.8)]
valid1 = new_data[int(df.shape[0]*0.8)+n_window:]
y_pred1 = np.reshape(y_pred1, [1, -1])

import datetime
dstart = datetime.datetime(2019,6,13)
dnow = datetime.datetime(2019,6,16)
plt.xlim(dstart, dnow)
valid1['Predictions'] = y_pred1[0]
plt.xlabel('Date')
plt.ylabel('Average Wind Speed')
plt.plot(train1['Direction'])
plt.plot(valid1['Direction'])
line2=plt.plot(valid1['Predictions'] )
import matplotlib.patches as mpatches
patch=mpatches.Patch(color='green', label='Predicted Wind Direction')
plt.legend(line2,handles=[patch],loc=2,fontsize=10)
plt.show()

plt.plot(np.array(valid1['Direction']))
plt.plot(y_pred1[0])

import math
from sklearn.metrics import mean_squared_error

testScore1 = math.sqrt(mean_squared_error(y_pred1[0], np.array(valid1['Direction'])))
print('Test Score: %.2f RMSE' % (testScore1))

np.savetxt('dir.csv', (prediction1[:24]))