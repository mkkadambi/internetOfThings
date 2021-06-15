
from boltiot import Sms, Bolt
import json, time
import conf


max_light = 800
min_light = 100

my_bolt = Bolt(conf.API_KEY, conf.DEVICE_NAME)

sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)


light_response_counter = 0
online_response_counter = 0
while (True):
 response =  my_bolt.isOnline()

 print("is online = ", type(response), response)

 json_response = json.loads(response)
 print("is online json=", json_response)
 if (json_response['value'] == 'offline'):
  response = sms.send_sms('Light Sensor is offline. Please check!')
  #print('Twilio response =', response)
 elif (json_response['success'] == 0):
  # There may be a network issue between this box and Bolt cloud
  online_response_counter += 1
  if (online_response_counter > 5):
   # send an sms for loss of communication with Bolt cloud
   response = sms.send_sms('There may be an issue with Bolt cloud, will continue to retry')
   #print('Twilio response =', response)
 else:
  online_response_counter = 0
  light_response = my_bolt.analogRead('A0')
  light_response = json.loads(light_response)
  print('light repsonse = ', light_response)
  if (light_response['success'] == 0):
   light_response_counter += 1
   if (light_response_counter > 5):
    response =sms.send_sms('Could not get light reading from sensor although it shows as being online')
    #print('Twilio response =', response) 
  else:
   light_response_counter = 0
   # the sensor shows 1024 for no light and 0 for fully illuminiated light
   light_response_value  = 1024 - int(light_response['value'])
   print('Light value =', light_response_value)

   if (light_response_value > max_light): 
    response = sms.send_sms('Too much light, value=' + str(light_response_value))
    #print('Twilio response = ', response)
   if (light_response_value < min_light):
    response = sms.send_sms('Very less light, value=' + str(light_response_value))
    #print('Twilio response= ', response)
 time.sleep(10)

