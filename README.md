# Wirepas-Python-sample

<!-- MarkdownTOC levels="1,2,3" autolink="true"  -->

- [Introduction](#introduction)
- [Technical Description](#technical-description)
- [Solution](#solution)
  - [Description](#description)
  - [Overview](#overview)

# Introduction
This repository provide an integration sample to use the Blue MESH tags provided by ELA Innovation. You will find here a Visual Studio 2019 project (you can download the VS 2019 Community [here](https://visualstudio.microsoft.com/fr/downloads/)) using WPF and C# to define an simple User Interface to get data from Wirepas MESH Network using Blue MESH from ELA Innovation.

# Technical Description
Before running and starting the project, you need to understand the Wirepas Technology, the network and the place of ELA Blue MESH Tags in the Wirepas Network. If you are a developper, you can consult the different Wirepas Github repository [here](https://github.com/wirepas) to understand the Network, the topology, the different tools requiered to build a Wirepas MESH infrastructure. But if you are already informed, there you can continue and use this project and the tag you receoved from ELA to run this project and try to get information from your Blue MESH.

First, you need to be sure that your Wirepas Gateway publish the network information on a MQTT Broker. You can use software like [MQTT Box](http://workswithweb.com/mqttbox.html) for Windows, [Mosquitto](https://mosquitto.org) for Unix to test your data. You need to install a MQTT Broker on you local network to publish and get the data from the network. To install a broker on Unix device, you can find more information [here](https://www.instructables.com/Installing-MQTT-BrokerMosquitto-on-Raspberry-Pi/). Then, you can conncet to your broker and subscribe to a main topic (for example #) but you can find more information about the wirepas topic [here](https://github.com/wirepas/backend-apis/blob/master/gateway_to_backend/README.md)

Then, this program the [Paho MQTT](https://pypi.org/project/paho-mqtt/) nuget to implement a MQTT Client and get the data publish on the MQTT Broker. Only MQTTClient object from the library is used on this example to use a client object to get the data.

# Prerequist
Before starting to use the program, it's necessary to install the requiered components to start your integration for this example and get data from Blue MESH tags. You need:
- Python 3.7
- paho-mqtt
- grpc

First of all be sure that your raspberry is up to date by executing the following commands:
```bash
   sudo apt-get update
```

Then install python 3.7; you may need to use pip3:
```bash
   sudo apt-get install python3-pip libglib2.0-dev
```
