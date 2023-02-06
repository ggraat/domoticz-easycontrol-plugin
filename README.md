# Bosch Easycontrol Domoticz plugin
Domoticz plugin that exposes information from the Bosch Easycontrol CT200 Thermostat in Domoticz using the [Bosch XMPP](https://github.com/robertklep/bosch-xmpp) bridge.

## Devices
The plugin adds the following devices to Domoticz:
* Room temperature
* Heating setpoint
* Actual supply temperature
* Supply temperature setpoint
* Humidity indoor
* Outdoor temperature

The devices are updated every minute.

## Configuration
The plugin needs to know where the Bosch XMPP is running (in bridge mode, see https://github.com/robertklep/bosch-xmpp#http-bridge). Provide the address (e.g. 127.0.0.1) and port (default: 3000). 

You can also turn on debugging to get some more information on what is happening.

## Disclaimer
This is a simple plugin based on my very basic knowledge of both Domoticz and Python. So use it at your own risk. :)
