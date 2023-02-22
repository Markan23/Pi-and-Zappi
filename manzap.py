#!/usr/bin/python
import time
import requests
from   requests.auth import HTTPDigestAuth
import json
import requests
import RPi.GPIO as GPIO
time.sleep(10)
Solarp = 0
Gridp = 0
switch = 0
loop = 0
good = 0

Red_LED_PIN = 8
Green_LED_PIN = 10
Green2_LED_PIN = 12

Off = 'cm?cmnd=Power%20Off'
On = 'cm?cmnd=Power%20On'
h2_url = 'http://192.168.1.251/'
h1_url = 'http://192.168.1.252/'

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(Red_LED_PIN, GPIO.OUT)
GPIO.setup(Green_LED_PIN, GPIO.OUT)
GPIO.setup(Green2_LED_PIN, GPIO.OUT)

username    = 'you hub serial number'
password    = 'Your password'
eddi_url    = 'https://s18.myenergi.net/cgi-jstatus-E'
zappi_url   = 'https://s18.myenergi.net/cgi-jstatus-Z'
harvi_url   = 'https://s18.myenergi.net/cgi-jstatus-H'
status_url  = 'https://s18.myenergi.net/cgi-jstatus-*'

dayhour_url = 'https://s18.myenergi.net/cgi-jdayhour-Z15536718-2021-10-20'

def catch_fail_html(testhtml):
    try:
        response = requests.get(testhtml, timeout=3)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Request to website failed ", e)
        # handle the exception here, such as retrying the request or using a backup data source
    else:
        # the request was successful and you can use the response
        print("website response ", response.text)

    return

def access_server(url_request):
  good = 0
  headers = {'User-Agent': 'Wget/1.14 (linux-gnu)'}
  try:
      r = requests.get(url_request, headers = headers, auth=HTTPDigestAuth(username, password), timeout=10)
      r.raise_for_status()
  except requests.exceptions.RequestException as e:
      print("Request to website failed ", e)
      # handle the exception here, such as retrying the request or using a backup data source
  else:
      # the request was successful and you can use the response
      print("server response ", r.text)
  if (r.status_code == 200):
      print ("") #"Login successful..")
  elif (r.status_code == 401):
      print ("Login unsuccessful!!! ")
      quit()
  else:
      logging.info("Login unsuccessful, returned code: " + r.status_code)
      quit()
  #print (r.json())
  good = 1
  return r.json()

def compare_solar_to_grid(solar, grid):
  GPIO.output(Red_LED_PIN, GPIO.LOW)
  GPIO.output(Green_LED_PIN, GPIO.LOW)
  GPIO.output(Green2_LED_PIN, GPIO.LOW)
  if grid < 0:
    # turn on 2 green LEDs
    GPIO.output(Green_LED_PIN, GPIO.HIGH)
    GPIO.output(Green2_LED_PIN, GPIO.HIGH)
    print("Turning on 2 green LEDs")
  elif solar == 0:
    # turn off 2 green LEDs and turn on red LED
    GPIO.output(Red_LED_PIN, GPIO.HIGH)
    print("Turning off 2 green LEDs and turning on red LED")
  elif solar > 25:
    # turn off red LED and turn on 1 green LED
    GPIO.output(Green_LED_PIN, GPIO.HIGH)
    print("Turning off red LED and turning on 1 green LED")
# end-of-function definition

catch_fail_html(h2_url+Off)
catch_fail_html(h1_url+Off)

GPIO.output(Red_LED_PIN, GPIO.HIGH)
GPIO.output(Green2_LED_PIN, GPIO.HIGH)
GPIO.output(Green_LED_PIN, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(Red_LED_PIN, GPIO.LOW)
GPIO.output(Green2_LED_PIN, GPIO.LOW)
GPIO.output(Green_LED_PIN, GPIO.LOW)

while loop == 0:
    print("loop start")
    response_data = access_server(harvi_url)
    for item in response_data['harvi']:
       Solarp =  item['ectp1']
       if Solarp < 65:
          Solarp = 0
          switch = 0

    while Solarp != 0:
        compare_solar_to_grid(Solarp, Gridp)
        response_data = access_server(zappi_url)
        for item in response_data['zappi']:
            print ("Query date: ", item['dat'])
            print ("Query time: ", item['tim'])
            Gridv = item['vol']/10
            Gridf = item['frq']
            Gridp = item['grd']

        response_data = access_server(harvi_url)
        for item in response_data['harvi']:
           Solarp =  item['ectp1']
           if Solarp < 65:
              Solarp = 0

        house = Gridp+Solarp
        Excessp = Solarp-house
        if Solarp-house <=0:
           Excessp = 0
        #print ("Grid Voltage:",Gridv,"Vac")
        #print ("Grid Frequency:",Gridf,"Hz")
        print ("Grid Power:",Gridp,"W")
        print ("Solar Power:",Solarp,"W")
        print ("House is using: ", house,"W")
        print ("Spare: ", Excessp,"W")

        compare_solar_to_grid(Solarp, Gridp)


        if  switch == 1 and (Gridp < -300):
            catch_fail_html(h2_url+On)
            switch = 2
            time.sleep(5)

        if  switch == 0 and (Gridp < -300):
            catch_fail_html(h1_url+On)
            switch = 1
            time.sleep(5)

        if  switch == 2 and (Gridp > 200):
            catch_fail_html(h2_url+Off)
            switch = 1
            time.sleep(5)

        if  switch == 1 and (Gridp > 200):
            catch_fail_html(h1_url+Off)
            switch = 0
            time.sleep(5)

        if switch  == 0:
            catch_fail_html(h1_url+Off)
            catch_fail_html(h2_url+Off)
        time.sleep(30)
    print("post sleep")
    elapsed_time = 0
    compare_solar_to_grid(Solarp, Gridp)
    while elapsed_time <= 100:
        if elapsed_time == 0:
            start_time = time.time()
        GPIO.output(Red_LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(Red_LED_PIN, GPIO.LOW)
        time.sleep(1)
        elapsed_time = time.time()-start_time
