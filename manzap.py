#!/usr/bin/python
import time
import requests
from   requests.auth import HTTPDigestAuth
import json
import requests
time.sleep(10)

username    = '(serial number of Harvi)'
password    = '(Password for Harvi)'
eddi_url    = 'https://s18.myenergi.net/cgi-jstatus-E'
zappi_url   = 'https://s18.myenergi.net/cgi-jstatus-Z'
harvi_url   = 'https://s18.myenergi.net/cgi-jstatus-H'
status_url  = 'https://s18.myenergi.net/cgi-jstatus-*'
dayhour_url = 'https://s18.myenergi.net/cgi-jdayhour-Z15536718-2021-10-20'

switch = 0
loop = 0

def access_server(url_request):
  headers = {'User-Agent': 'Wget/1.14 (linux-gnu)'}
  r = requests.get(url_request, headers = headers, auth=HTTPDigestAuth(username, password), timeout=10)
  if (r.status_code == 200):
      print ("") #"Login successful..")
  elif (r.status_code == 401):
      print ("Login unsuccessful!!! ")
      quit()
  else:
      logging.info("Login unsuccessful, returned code: " + r.status_code)
      quit()
  #print (r.json())
  return r.json()

# end-of-function definition
res = requests.post("http://192.168.1.xxx/cm?cmnd=Power%20Off")
res = requests.post("http://192.168.1.xxx/cm?cmnd=Power%20Off")

while loop == 0:
    print("Start of outer loop")
    response_data = access_server(harvi_url)
    for item in response_data['harvi']:
       Solarp =  item['ectp1']
       if Solarp < 50:
          Solarp = 0
		  switch = 0
		  
    while Solarpp != 0:
	    print("Start of inner loop")
        response_data = access_server(zappi_url)
        for item in response_data['zappi']:
            Gridv = item['vol']/10
            Gridf = item['frq']
            Gridp = item['grd']

        response_data = access_server(harvi_url)
        for item in response_data['harvi']:
           Solarp =  item['ectp1']
           if Solarp < 50:
              Solarp = 0

        house = Gridp+Solarp
        Excessp = Solarp-house
        if Solarp-house <=0:
           Excessp = 0
        print ("Grid Voltage:",Gridv,"Vac")
        print ("Grid Frequency:",Gridf,"Hz")
        print ("Grid Power:",Gridp,"W")
        print ("Solar Power:",Solarp,"W")
        print ("House is using: ", house,"W")
        print ("Spare: ", Excessp,"W")

        if  switch == 1 and (Gridp < -300):
            print("Heater 2 on")
            res = requests.post("http://(ip address of sonoff socket 2)/cm?cmnd=Power%20On")
            switch = 2

        if  switch == 0 and (Gridp < -300):
            print("Heater 1 on")
            res = requests.post("http://(ip address of sonoff socket 1)/cm?cmnd=Power%20On")
            switch = 1
            time.sleep(5)

        if  switch == 2 and (Gridp > 200):
            print("Heater 2 off")
            res = requests.post("http://(ip address of sonoff socket 2)/cm?cmnd=Power%20Off")
            switch = 1
            time.sleep(5)

        if  switch == 1 and (Gridp > 200):
            print("Heater 1 off")
            res = requests.post("http://(ip address of sonoff socket 1)/cm?cmnd=Power%20Off")
            switch = 0
        # End of inner loop
        time.sleep(20)
    time.sleep(600)
