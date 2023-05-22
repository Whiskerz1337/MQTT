# MQTT

A 'Sensor' for sending CPU and RAM usage data to ThingSpeak MQTT broker.

## Installation

I'd recommend using a Kali Linux VM for this as WireShark will be useful for confirming encryption, and git should already be installed.

1. Download with ```git clone https://github.com/Whiskerz1337/MQTT.git```
2. Open .env (hidden file)
3. Add your username from ThingSpeak inside the empty mqtt_username string
4. Add your client ID (same as username) inside the empty mqtt_client_ID string
5. Add your password from ThingSpeak inside the empty mqtt_password string
6. Add your channel ID from ThingSpeak inside the empty channel_ID string
7. Save the file (.env)

## Usage

1. Run the program with ```python main.py``` 
2. Set the number of messages to send (must be a whole number)
3. Set the interval between collection/messages (must be a whole number)
4. Wait for the program to complete
5. Check for updated data on ThingSpeak.
