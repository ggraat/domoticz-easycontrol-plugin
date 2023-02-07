"""
<plugin key="domoticz-easycontrol-plugin" name="Bosch Easycontrol (CT200) plugin" author="ggraat" version="0.0.1">
    <description>
        <h2>Bosch Easycontrol (CT200) plugin</h2><br/>
        Basic plugin that exposes information from the Bosch Easycontrol CT200 Thermostat in Domoticz using the Bosch XMPP bridge
        <h3>Devices</h3>
        The following devices are created
        <ul style="list-style-type:square">
            <li>Room temperature</li>
            <li>Heating setpoint</li>
            <li>Actual supply temperature</li>
            <li>Supply temperature setpoint</li>
            <li>Humidity indoor</li>
            <li>Outdoor temperature</li>
        </ul>
        <h3>Configuration</h3>
        Configure where the Bosch XMPP is running
    </description>
     <params>
        <param field="Address" label="Bridge Address" required="true" default="127.0.0.1"/>
        <param field="Port" label="Bridge Port" required="true" default="3000"/>
        <param field="Mode6" label="Debug">
            <options>
                <option label="True" value="2"/>
                <option label="False" value="0" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import requests


class EasycontrolPlugin:
    class DomoticzThermoDevice:
        def __init__(self, unit, endpoint, name, typename=None, type=None, subtype=None):
            if typename is not None:
                self.device = Domoticz.Device(Unit=unit, Name=name, TypeName=typename)
            else:
                self.device = Domoticz.Device(Unit=unit, Name=name, Type=type, Subtype=subtype)
            self.endpoint = endpoint

    runAgain = 6
    thermoDevices = ()

    def __init__(self):
        return

    def onStart(self):
        if (Parameters["Mode6"] == "2"):
            Domoticz.Debugging(2)
        else:
            Domoticz.Debugging(0)

        self.thermoDevices = (
            self.DomoticzThermoDevice(1, "/zones/zn1/temperatureActual", "Room temperature", "Temperature"),
            self.DomoticzThermoDevice(2, "/zones/zn1/temperatureHeatingSetpoint", "Heating setpoint", None, 242, 1),
            self.DomoticzThermoDevice(3, "/heatSources/actualSupplyTemperature", "Actual supply temperature",
                                      "Temperature"),
            self.DomoticzThermoDevice(4, "/heatingCircuits/hc1/supplyTemperatureSetpoint",
                                      "Supply temperature setpoint", None, 242, 1),
            self.DomoticzThermoDevice(5, "/system/sensors/humidity/indoor_h1", "Humidity indoor", "Humidity"),
            self.DomoticzThermoDevice(6, "/system/sensors/temperatures/outdoor_t1", "Outdoor temperature",
                                      "Temperature"),
        )

        if (len(Devices) == 0):
            for thermoDev in self.thermoDevices:
                thermoDev.device.Create()
                Domoticz.Log("Created " + thermoDev.device.Name + " device")
                self.updateDeviceValue(thermoDev)
        else:
            Domoticz.Debug("Devices already exist" + str(Devices))

    def onStop(self):
        return

    def onConnect(self, Connection, Status, Description):
        return

    def onMessage(self, Connection, Data):
        return

    def onCommand(self, Unit, Command, Level, Hue):
        return

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        return

    def onDisconnect(self, Connection):
        return

    def onHeartbeat(self):
        self.runAgain = self.runAgain - 1
        if self.runAgain <= 0:
            for thermoDev in self.thermoDevices:
                self.updateDeviceValue(thermoDev)
            self.runAgain = 6
        else:
            Domoticz.Debug("onHeartbeat called, run again in " + str(self.runAgain) + " heartbeats.")

    def updateDeviceValue(self, thermodevice: DomoticzThermoDevice):
        url = "http://" + Parameters["Address"] + ":" + Parameters["Port"] + "/bridge" + thermodevice.endpoint
        request = requests.get(url)
        value = request.json()["value"]
        Domoticz.Debug("Going to set value " + str(value) + " on device " + thermodevice.device.Name)
        thermodevice.device.Update(int(value), str(value))


global _plugin
_plugin = EasycontrolPlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)


def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)


def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)


def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)


def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()
