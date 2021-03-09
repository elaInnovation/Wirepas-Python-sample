# Wirepas-Python-sample

<!-- MarkdownTOC levels="1,2,3" autolink="true"  -->

- [Introduction](#introduction)
- [Technical Description](#technical-description)
- [Prerequist](#prerequist)
- [Sample](#sample)

# Introduction
This repository provide an integration sample to use the Blue MESH tags provided by ELA Innovation. You will find here python scripts and description to decode data received from Wirepas Network using MQTT Broker. You can edit your python file using text editor like Notepad or Notepad++, or using specific ID like Visual Studio Code [here](https://code.visualstudio.com/download). Then you can decode Wirepas MESH Network information and payload using Blue MESH from ELA Innovation.

# Technical Description
Before running and starting the project, you need to understand the Wirepas Technology, the network and the place of ELA Blue MESH Tags in the Wirepas Network. If you are a developper, you can consult the different Wirepas Github repository [here](https://github.com/wirepas) to understand the Network, the topology, the different tools requiered to build a Wirepas MESH infrastructure. But if you are already informed, there you can continue and use this project and the tag you receoved from ELA to run this project and try to get information from your Blue MESH.

First, you need to be sure that your Wirepas Gateway publish the network information on a MQTT Broker. You can use software like [MQTT Box](http://workswithweb.com/mqttbox.html) for Windows, [Mosquitto](https://mosquitto.org) for Unix to test your data. You need to install a MQTT Broker on you local network to publish and get the data from the network. To install a broker on Unix device, you can find more information [here](https://www.instructables.com/Installing-MQTT-BrokerMosquitto-on-Raspberry-Pi/). Then, you can conncet to your broker and subscribe to a main topic (for example #) but you can find more information about the wirepas topic [here](https://github.com/wirepas/backend-apis/blob/master/gateway_to_backend/README.md)

Then, this program the [Paho MQTT](https://pypi.org/project/paho-mqtt/) nuget to implement a MQTT Client and get the data publish on the MQTT Broker. Only MQTTClient object from the library is used on this example to use a client object to get the data.

Figure 1 illustrates how we can use Backend Client and how we can use this sample

![here_schematics](https://github.com/elaInnovation/Wirepas-Python-sample/blob/master/Images/wirepas_explain_sample_01.png)

# Prerequist
Before starting to use the program, it's necessary to install the requiered components to start your integration for this example and get data from Blue MESH tags. You need:
- Python 3.7
- git
- paho-mqtt
- grpc / protoc

First of all be sure that your raspberry is up to date by executing the following commands:
```bash
   sudo apt-get update
```

## Install Python
Then install python 3.7; you may need to use pip3:
```bash
   sudo apt-get install python3-pip libglib2.0-dev
```

## Install Git
If you have not yet install git, please do it by enterring the following command line:
```bash
   sudo apt-get install git
```

## Install Paho MQTT
The latest stable version is available in the Python Package Index (PyPi) and can be installed using:
```bash
  pip3 install paho-mqtt
```

To obtain the full code, including examples and tests, you can clone the git repository:
```bash
  git clone https://github.com/eclipse/paho.mqtt.python
```

Once you have the code, it can be installed from your repository as well:
```bash
  cd paho.mqtt.python
  python setup.py install
```

There, you're ready to use the MQTT tools and start to develop your project wit the Paho Mqtt layer.

## Install Protobuff
To deceode the payload, you need to install and use protobuff. You can find more documentation to proceed in Python [here](https://developers.google.com/protocol-buffers/docs/pythontutorial). However, we explain how to do it in the next paragraph. But before codinf, you need to install all the dependencies to develop using Protobuf messages. 
```bash
  sudo pip3 install grpcio
  sudo pip3 install grpcio-tools
```

With **protoc** you'll be ready to build your proto file and generate the class requiered to decode your Protobuff encoded messages.

# Sample
Here, one more step is missing to start your sample. You need to use the **proto file** provided in this sample to generate the python class usefull to decode your payload. To proceed, you need to use **protoc** to generate the file. In the main folder, enter the following command line:
```bash
  sudo python3 -m grpc_tools.protoc -I. --python_out=. ./proto/ElaCommon.proto
  sudo python3 -m grpc_tools.protoc -I. --python_out=. ./proto/WirepasMessages.proto
```

Now you're ready to start the sample and decode the message contained in the mqtt payload. To run the program, you need to specify yout broker **IP address** or the **hostname** as argument. You can run it by executing the following command line: (replace ***<your_ip_address>*** by your target broker)
```bash
  sudo python3 wirepas_sample_decode.py <your_ip_address>
```

The main program is here to check your input parameter and run the MQTT client using **Paho.MQTT**. The following python lines are necessary to create your MQTT Client, associate the callback function, and connect ti the broker:
```python
  #
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message

  client.connect(broker_ip_address, 1883, 60)
```

We subscribe to the "#" topic, this mean that all message received from the broker will be visible in the **on_message** function. This subscribtion append in the **on_connect** function:
```python
  # Subscribing in on_connect() means that if we lose the connection and
  # reconnect then subscriptions will be renewed.
  client.subscribe("#")
```

There, all message received from the broker are processed in the **on_message** funciton. The payload received from the different topics are encoded with **Proto Buffer**. To interpret it, you need to decode the content using **Proto Buffer**, the **proto files** and the **classes** generated with **protoc** tool. In the python code, we will create a **GenericMessage** object and use the function **ParseFromString** to feed the object with the different informations:
```python
  print(">Create Generic Message")
  message = GenericMessage()
  genericMessage = message.ParseFromString(msg.payload)
  decodeMessage(message)
```

In the output, we display this information. Before decoding and received from MQTT, you will have this kind on information:
```bash
==========NEW DATA RECEIVED==========
Topic : gw-event/received_data/RPiSW_A807B5_5/sink1/11012021/110/110
Data : b'\nIBG\n!\n\x0eRPiSW_A807B5_5\x12\x05sink1\x18\xef\xdc\xa2\x8f\xb2\xec\xfc\xa1x\x10\xbf\xe7!\x18\x05 n(n0\xebG8\xb8\xb2\xba\x95\x81/@\x01J\n\x03\x04?\x00\x92\x07\x01\x02\xa1\x0bX\x03'

==========NEW DATA RECEIVED==========
Topic : gw-event/received_data/RPiSW_A807B5_5/sink1/11012021/100/100
Data : b'\nIBG\n"\n\x0eRPiSW_A807B5_5\x12\x05sink1\x18\xda\xbb\xc6\x92\xd6\x8d\xc0\xf8\xbb\x01\x10\xfc\x95\xea\x03\x18\x05 d(d0\xc798\xf2\xe4\xbe\x95\x81/@\x01J\x08\x02\x02\xd0\t\x01\x02\xaf\x0bX\x02'
```

And when we decode it, the GenericMessage and all information will be handle in **packet_received_event**. The two following sample are the **Proto Buffer** deserialization in **GenereicMessage** object. The first one is a sample of **Blue MESH RHT**:
```bash
message : packet_received_event {
  header {
    gw_id: "RPiSW_A807B5_5"
    sink_id: "sink1"
    event_id: 8666037715087175279
  }
  source_address: 553919
  destination_address: 5
  source_endpoint: 110
  destination_endpoint: 110
  travel_time_ms: 9195
  rx_time_ms_epoch: 1615221135672
  qos: 1
  payload: "\003\004?\000\222\007\001\002\241\013"
  hop_count: 3
}
```
The second one is for a **Blue MESH T**:
```bash
message : packet_received_event {
  header {
    gw_id: "RPiSW_A807B5_5"
    sink_id: "sink1"
    event_id: 8666037715087175279
  }
  source_address: 553919
  destination_address: 5
  source_endpoint: 110
  destination_endpoint: 110
  travel_time_ms: 9195
  rx_time_ms_epoch: 1615221135672
  qos: 1
  payload: "\003\004?\000\222\007\001\002\241\013"
  hop_count: 3
}
```

All the information you need to decode using the **Blue MESH documentation** are handle in the payload buffer. you can find the Blue MESH documentation on ELA Innovation website. But there, ou will find in this sampple the python functions to decode the informations, for temperature:
```python
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
```

For temperature and Humidity:
```python
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
```

For counter functions like Blue MESH MAG, MOV, DI, DO AT:
```python
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
```
