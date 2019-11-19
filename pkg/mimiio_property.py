"""xmimiio adapter for Mozilla WebThings Gateway."""

from gateway_addon import Property
import socket


class PhilipsBulbProperty(Property):
    """Yeelight property type."""

    def __init__(self, device, name, description, value):
        """
        Initialize the object.
        device -- the Device this property belongs to
        name -- name of the property
        description -- description of the property, as a dictionary
        value -- current value of this property
        """
        Property.__init__(self, device, name, description)
        self.set_cached_value(value)

    def set_value(self, value):
        """
        Set the current value of the property.
        value -- the value to set
        """
        try:
            self.device.update_properties()

            if self.device.is_on():
                if self.name == 'on':
                    if value:
                        pass
                    else:
                        self.device.bulb.off()
                elif self.name == 'level':
                    value = max(value, self.description['minimum'])
                    value = min(value, self.description['maximum'])
                    self.device.bulb.set_brightness(value)
                elif self.name == 'colorTemperature':
                    value = max(value, self.description['minimum'])
                    value = min(value, self.description['maximum'])
                    self.device.bulb.set_color_temperature(value)
                elif self.name == 'scene':
                    value = max(value, self.description['minimum'])
                    value = min(value, self.description['maximum'])
                    self.device.bulb.set_scene(value)
                else:
                    return
            elif self.name == 'on':
                self.device.bulb.on()
        except socket.error:
            return

        self.set_cached_value(value)
        self.device.notify_property_changed(self)

    def update(self):
        """Update the current value, if necessary."""
        if self.name == 'on':
            value = self.device.is_on()
        elif self.name == 'scene':
            value = self.device.scence()
        elif self.name == 'level':
            value = self.device.brightness()
        elif self.name == 'colorTemperature':
            value = self.device.color_temperature()
        else:
            return

        if value != self.value:
            self.set_cached_value(value)
            self.device.notify_property_changed(self)

