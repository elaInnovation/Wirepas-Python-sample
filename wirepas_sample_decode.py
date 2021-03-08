import paho.mqtt.client as mqtt
import sys
import binascii

# Constant definition
DESTINATION_ENDPOINT_MOVEMENT = 160
DESTINATION_ENDPOINT_TEMPERATURE = 100
DESTINATION_ENDPOINT_TEMPERATURE_HUMIDITY = 110
DESTINATION_ENDPOINT_DIGITAL_INPUT = 120
DESTINATION_ENDPOINT_DIGITAL_OUTPUT = 130
DESTINATION_ENDPOINT_ANTI_TEARING = 140
DESTINATION_ENDPOINT_MAGNETIC_DETECTION = 150

# Protos import
import proto.ElaCommon_pb2
import proto.WirepasMessages_pb2
from proto.WirepasMessages_pb2 import GenericMessage
from proto.WirepasMessages_pb2 import WirepasMessage

# decode the data in two complement
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

# decode the temperature
def decodeTemperature(payload):
    print("[Payload]\t[Temperature]\tRaw Payload : ", binascii.hexlify(payload))
    buffer = binascii.hexlify(payload)
    if(len(payload) >= 4):
        type = payload[0]
        length_data = payload[1]
        temp_lsb = payload[2]
        temp_msb = payload[3]
        if(2 == type and 2 == length_data):
            temperature = (twos_comp((temp_msb << 8) + temp_lsb, 16)) / 100
            print("[Payload]\t[Temperature]\tTemperature value : ", temperature, " °C")
        else:
            print("[Payload]\t[Temperature]\tThis is not a temperature data")
            print("[Payload]\t[Temperature]\tType : ", type)

# decode the temperature
def decodeTemperatureAndHumidity(payload):
    print("[Payload]\t[Temperature//Humidity]\tRaw Payload : ", binascii.hexlify(payload))
    buffer = binascii.hexlify(payload)
    if(len(buffer) >= 6):
        type = payload[0]
        length_data = payload[1]
        humi_lsb = payload[2]
        humi_msb = payload[3]
        temp_lsb = payload[4]
        temp_msb = payload[5]
        if(3 == type and 4 == length_data):
            temperature = (twos_comp((temp_msb << 8) + temp_lsb, 16)) / 100
            humidity = humi_lsb
            print("[Payload]\t[Temperature//Humidity]\tTemperature value : ", temperature, " °C")
            print("[Payload]\t[Temperature//Humidity]\tHumidity value : ", humidity, " %")
        else:
            print("[Payload]\t[Temperature//Humidity]\tThis is not a temperature data")
            print("[Payload]\t[Temperature//Humidity]\tType : ", type)

# decode counter for magnetic, movement, digital output, digital input, anti tearing 
def decodeStateAndCounter(payload):
    print("[Payload]\t[State and Count]\tRaw Payload : ", binascii.hexlify(payload))
    buffer = binascii.hexlify(payload)
    if(len(buffer) >= 8):
        type = payload[0]
        length_data = payload[1]
        state_lsb = payload[2]
        state_msb = payload[3]
        count_b0 = payload[4]
        count_b1 = payload[5]
        count_b2 = payload[6]
        count_b3 = payload[7]
        if( (4 == type or 5 == type or 6 == type or 7 == type or 8 == type) and 6 == length_data):
            counter = (count_b3 << 32) +(count_b2 << 16) + (count_b1 << 8) + count_b0
            state = state_lsb
            print("[Payload]\t[State and Count]\tState value : ", state)
            print("[Payload]\t[State and Count]\tCounter value : ", counter)
            if 4 == type:
                print("[Payload]\t[State and Count]\tDigital Input")
            elif 5 == type:
                print("[Payload]\t[State and Count]\tDigital Output")
            elif 6 == type:
                print("[Payload]\t[State and Count]\tAnti Tearing")
            elif 7 == type:
                print("[Payload]\t[State and Count]\tMagnetic")
            elif 8 == type:
                print("[Payload]\t[State and Count]\tMovement")
        else:
            print("[Payload]\t[State and Count]\tThis is not a counter // state data")
            print("[Payload]\t[State and Count]\tType : ", type)

# Common function to decode a wirepas payload
def decodeWirepasPayload(packet_received_event):
    print("[Payload]\tTry decode payload from GenericMessage.Wirepas")
    if packet_received_event is None:
        print("[Payload]\tNO PAYLOAD FOUND !!!")
    else:
        if DESTINATION_ENDPOINT_TEMPERATURE == packet_received_event.destination_endpoint:
            print("[Payload]\t[Blue MESH]\tTemperature MESH Sensor")
            decodeTemperature(packet_received_event.payload)
        elif DESTINATION_ENDPOINT_TEMPERATURE_HUMIDITY == packet_received_event.destination_endpoint:
            print("[Payload]\t[Blue MESH]\tTemperature and Humidity MESH Sensor")
            decodeTemperatureAndHumidity(packet_received_event.payload)
        elif DESTINATION_ENDPOINT_DIGITAL_INPUT == packet_received_event.destination_endpoint:
            print("[Payload]\t[Blue MESH]\tDigital Input MESH Sensor")
            decodeStateAndCounter(packet_received_event.payload)
        elif DESTINATION_ENDPOINT_DIGITAL_OUTPUT == packet_received_event.destination_endpoint:
            print("[Payload]\t[Blue MESH]\tDigital Output MESH Sensor")
            decodeStateAndCounter(packet_received_event.payload)
        elif DESTINATION_ENDPOINT_ANTI_TEARING == packet_received_event.destination_endpoint:
            print("[Payload]\t[Blue MESH]\tAnti Tearing MESH Sensor")
            decodeStateAndCounter(packet_received_event.payload)
        elif DESTINATION_ENDPOINT_MAGNETIC_DETECTION == packet_received_event.destination_endpoint:
            print("[Payload]\t[Blue MESH]\tMagnetic MESH Sensor")
            decodeStateAndCounter(packet_received_event.payload)
        elif DESTINATION_ENDPOINT_MOVEMENT == packet_received_event.destination_endpoint:
            print("[Payload]\t[Blue MESH]\tMovement MESH Sensor")
            decodeStateAndCounter(packet_received_event.payload)
        else:
            print("[Payload]\t[Blue MESH]\tThis message is not supporter by this Python Script")

# Common function to decode wirepas message
def decodeMessage(message):
    if message is None:
        print("[Decode]\tNo message to decode")
    else:
        print("[Decode]\tDecoding wirepas message")
        if message.wirepas is None:
            print("[Decode]\tNo wirepas message")
        else:
            print("[Decode]\t message : " + str(message.wirepas))
            decodeWirepasPayload(message.wirepas.packet_received_event)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("==========NEW DATA RECEIVED==========")
    print("Topic : " +  msg.topic)
    print("Data : " + str(msg.payload))
    #
    try:
        print(">Create Generic Message")
        message = GenericMessage()
        genericMessage = message.ParseFromString(msg.payload)
        decodeMessage(message)
        #print("Decoded : " + GenericMessage.ParseFromString(msg.payload))
    except Exception as e:
        print("[Exception]\tIncoming Message : " , e)
        print("[Exception]\tCannot decode message", sys.exc_info()[0])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.161", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
