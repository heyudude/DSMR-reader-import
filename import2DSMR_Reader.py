# Python3

import csv
import pandas as pd
import requests
import json
import datetime

APIKey = '*API*'
#csvMulti = pd.read_csv('multimeter_calender.csv') # electra
#csvMeter = pd.read_csv('meter_calender.csv') # Gas
csvMulti = pd.read_csv('mu.csv') # electra
csvMeter = pd.read_csv('me.csv') # Gas

def init_data():
  # filter the IDX for Electra and Gas (in this case 91 and 107 from Domoticz)
  fcsvMulti = csvMulti.loc[csvMulti['DeviceRowID'].isin([91])]
  del fcsvMulti['DeviceRowID']
  del fcsvMulti['Value1']
  del fcsvMulti['Value2']
  del fcsvMulti['Value3']
  del fcsvMulti['Value4']
  del fcsvMulti['Value5']
  del fcsvMulti['Value6']
  #print('Filtered Electra list:', fcsvMulti)

  fcsvMeter = csvMeter.loc[csvMeter['DeviceRowID'].isin([107])]
  del fcsvMeter['DeviceRowID']
  del fcsvMeter['Value']
  #print("Filtered Gas list:", fcsvMeter)

  #Create a new csv file :
  data = pd.merge(fcsvMulti,fcsvMeter)
  data.to_csv("merge_data.csv")

def write_response(timestamp):
    response = requests.post(
      'http://192.168.2.15/api/v2/datalogger/dsmrreading',
         headers={'X-AUTHKEY': APIKey},
     data={
       'electricity_currently_delivered': 0.000,
       'electricity_currently_returned': 0.000,
       'electricity_delivered_1': Del1,
       'electricity_returned_1': Ret1,
       'electricity_delivered_2': Del2,
       'electricity_returned_2': Ret2,
       'extra_device_timestamp': timestamp,
       'extra_device_delivered': Gas,
       'timestamp': timestamp
      }
    )

    if response.status_code != 201:
      print('Error: {}'.format(response.text))
    else:
      print('Created: {}'.format(json.loads(response.text)))

# main
init_data()
csvData = pd.read_csv('merge_data.csv')

for index, row in csvData.iterrows():
   print(row['Date'], row['Counter1'], row['Counter2'], row['Counter3'], row['Counter4'], row['Counter'])
   Del1 = int(row['Counter1'])/1000
   Ret1 = int(row['Counter2'])/1000
   Del2 = int(row['Counter3'])/1000
   Ret2 = int(row['Counter4'])/1000
   Gas  = int(row['Counter'])/1000

   DataDate = datetime.datetime.strptime(row['Date'], '%Y-%m-%d').strftime('%Y-%m-%d')
   timestamp = DataDate + ' 00:00:00+02'
   write_response(timestamp)
   DataDate = datetime.datetime.strptime(row['Date'], '%Y-%m-%d').strftime('%Y-%m-%d')
   timestamp = DataDate + ' 23:59:00+02'
   write_response(timestamp)

# EOF
