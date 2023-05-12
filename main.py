from dotenv import load_dotenv
import paho.mqtt.publish
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


  # Create the topic string.

  topic = "channels/" + channel_ID + "/publish"

  def on_message(client, userdata, message):

      if debug: 

        print("received message =",str(message.payload.decode("utf-8")))

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

    ##start loop to process received messages

    client.loop_start()

    if debug: 

      time.sleep(4)

      print("Subscribing to topic",topic)

    client.subscribe(topic)

    if debug: 

      time.sleep(3)

      print("Gathering 20 secs of CPU usage data")

    cpu_percent = psutil.cpu_percent(interval=20)

    ram_percent = psutil.virtual_memory().percent

    if debug:

      print("Sending message with payload now.")

    # build the payload string.

    payload = "field1=" + str(cpu_percent) + "&field2=" + str(ram_percent)

    # attempt to publish this data to the topic.

    client.publish(topic, payload) #expecting a message callback after this

  except Exception as e:

      print (e) 

  #if debug: 

  finally:

    time.sleep(2) # need to wait for the callback

    client.loop_stop()

  if debug:

    time.sleep(1)

    client.disconnect()

if __name__ == "__main__":
  main_function()
