from dotenv import load_dotenv
import paho.mqtt.publish
import sys
import psutil
import paho.mqtt.client as paho
import ssl
import time
import os

def main_function():
  debug = True
  load_dotenv()

  mqtt_username = os.getenv('mqtt_username')
  mqtt_client_ID = os.getenv('mqtt_client_ID')
  mqtt_password = os.getenv('mqtt_password')
  channel_ID = os.getenv('channel_ID')
  t_port = int(os.getenv('t_port'))
  mqtt_host = os.getenv('mqtt_host')

  topic = "channels/" + channel_ID + "/publish"

  print("This program will collect CPU and RAM usage data and send the data to ThingSpeak.\n")
  
  data_points = int(input("How many data points would you like to send to ThingSpeak? ( 5 - 30 recommended ): \n"))

  if data_points > 100:
    print("\nNote: Setting data points to maximum of 100...\n")
    data_points = 100

  interval_time = int(input("At what interval (in seconds) would you like to collect and send data ( 1 - 10 recommended ): \n"))

  if interval_time > 60:
    print("\nNote: Setting interval to maximum of 60 seconds...\n")
    interval_time = 60

  if interval_time > 10:
    print("Warning: Greater than 10 second delay added\n")
    match input("Proceed with long delay y/n: \n"):
      case 'n' | 'N' | 'no' | 'No' | 'NO':
        interval_time = int(input("\nAt what interval (in seconds) would you like to collect and send data ( 1 - 10 recommended ): \n"))
      case 'y' | 'Y' | 'yes' | 'Yes' | 'YeS' | 'YES':
        print(f"\nProceeding with long delay of {interval_time} seconds.")
      case _:
        sys.exit("\nUnexpected input. Exiting Program.")

  def on_message(client, userdata, message):
      if debug: 
        print("Sent data")
      else:
        print("<", end="")

  def on_log(client, userdata, level, buf):
      pass#print("log: ",buf)
    
  def on_connect(client, userdata, flags, rc):
      if debug:
        print("CONNACK received with code %d. - " % (rc), end="")
        if rc == 0:
          print("Connection successful!")
        if rc == 4:
          print("Connection refused - bad username or password")

  def on_subscribe(client, userdata, mid, granted_qos):
      if debug: 
        print("Subscribed! QOS=", granted_qos)

  def on_disconnect(client, userdata, rc):
    if rc == 0:
      if debug: 
        print("Intentional disconnection ACK") 
      else: 
        print(">", end="")
    if rc == 1:
      if debug:
        print("Other disconnection reason ACK")

  #define callbacks

  client = paho.Client(mqtt_client_ID) 
  client.on_message = on_message
  client.on_log = on_log
  client.on_connect = on_connect
  client.on_subscribe = on_subscribe
  client.on_disconnect = on_disconnect

  client.tls_set(ca_certs=None, certfile=None, keyfile=None, 
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None) #works fine over port 8883

  try:
    if debug: 
      print("connecting to broker")

    client.username_pw_set(mqtt_username, mqtt_password)
    client.connect(mqtt_host, t_port, 60)
      #expecting a callback on_connect
    
    client.loop_start()
    
    if debug: 
      time.sleep(4)
      print("Subscribing to topic",topic)
    client.subscribe(topic)
    
    if debug: 
      time.sleep(3)
      print("\nGathering " + str(data_points) + " data points of CPU and RAM usage at " + str(interval_time) + " second intervals...\n")
      print("Use CTRL+C to cancel early if required.\n")

    for i in range(data_points):  
      cpu_percent = psutil.cpu_percent(interval=1)  
      ram_percent = psutil.virtual_memory().percent  
      if debug:
          print(f"Gathering data {i+1}/{data_points}: CPU = {cpu_percent}, RAM = {ram_percent}")
      time.sleep(interval_time)  

      # Create payload
      payload = "field1=" + str(cpu_percent) + "&field2=" + str(ram_percent)
    
      client.publish(topic, payload)  

  except Exception as e:
      print (e) 

  finally:
    time.sleep(2) # need to wait for the callback
    client.loop_stop()
  if debug:
    time.sleep(1)
    client.disconnect()

if __name__ == "__main__":
  main_function()
