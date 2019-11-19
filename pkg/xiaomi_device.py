from gateway_addon import Device
import socket
import threading
import time

from .xiaomi_property import PhilipsBulbProperty

_POLL_INTERVAL = 5

class PhilipsBulb(Device):
    "xiaomi philips_bulb device"
    
    
    def __init__(self, adapter,_id, ip, token):
        """
        Initialize the object.
        adapter -- the Adapter managing this device
        _id -- ID of this device
        ip -- ip address for this device
        token --token  for this device
        """ 
        from miio.philips_bulb import PhilipsBulb   
        Device.__init__(self, adapter, _id)
        self._type = ['OnOffSwitch', 'Light','ColorControl']
        self.bulb =  PhilipsBulb(ip = ip, token = token)


        self.update_properties()

        self.properties['colorTemperature'] = PhilipsBulbProperty(
            self,
            'colorTemperature',
            {
                '@type': 'ColorTemperatureProperty',
                'label': 'Color Temperature',
                'type': 'integer',
                'unit': 'kelvin',
                'minimum': 1,
                'maximum': 100,
            },
            self.color_temperature())

        self.properties['level'] = PhilipsBulbProperty(
            self,
            'level',
            {
                '@type': 'BrightnessProperty',
                'label': 'Brightness',
                'type': 'integer',
                'unit': 'percent',
                'minimum': 1,
                'maximum': 100,
            },
            self.brightness())

        self.properties['on'] = PhilipsBulbProperty(
            self,
            'on',
            {
                '@type': 'OnOffProperty',
                'label': 'On/Off',
                'type': 'boolean',
            },
            self.is_on())

        self.properties['scene'] = PhilipsBulbProperty(
            self,
            'scene',
            {
                '@type': 'SceneProperty',
                'label': 'scene',
                'type': 'integer',
                'minimum': 1,
                'maximum': 4,
            },
            self.scence())

        t = threading.Thread(target=self.poll)
        t.daemon = True
        t.start()

    def poll(self):
        """Poll the device for changes."""
        while True:
            time.sleep(_POLL_INTERVAL)
            self.update_properties()

            for prop in self.properties.values():
                prop.update()

    def update_properties(self):
        """Update the cached properties."""
        try:
            self.bulb_properties = self.bulb.status()
        except socket.error:
            pass

    def scence(self):
        """Determine whether or not the light is dimmable."""
        return self.bulb_properties.scene()

    def is_on(self):
        """Determine whether or not the light is on."""
        return self.bulb_properties.is_on()  

    def color_temperature(self):
        """Determine the current color temperature."""
        return self.bulb_properties.color_temperature()

    def brightness(self):
        """Determine the current brightness of the light."""
        return self.bulb_properties.brightness()
