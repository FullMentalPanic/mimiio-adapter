"""mimiio adapter for Mozilla WebThings Gateway."""

from gateway_addon import Adapter, Database
from .mimiio_device import *


_TIMEOUT = 3

DeviceTypeDict = {
    'PhilipsZhiruiSmartLEDBulb': 'PhilipsBulb',
    'XiaomiMiRobotVacuum': 'vacuum',
}

class MimiioAdapter(Adapter):
    """Adapter for Xiaomi smart home devices."""

    def __init__(self, verbose=False):
        """
        Initialize the object.
        verbose -- whether or not to enable verbose logging
        """
        self.name = self.__class__.__name__
        Adapter.__init__(self,
                         'mimiio-adapter',
                         'mimiio-adapter',
                         verbose=verbose)
        self.pairing = False
        self.add_from_config()
     #   self.start_pairing(_TIMEOUT)

    def add_from_config(self):
        """Attempt to add all configured devices."""
        database = Database('mimiio-adapter')
        if not database.open():
            return
        

        config = database.load_config()
        database.close()
        if not config or 'Token' not in config or 'IPaddress' not in config:
            return
        if (config['Token'] is not '') and (config['IPaddress'] is not ''):
            self._add_device(config['DeviceType'], config['Token'], config['IPaddress'])
            
    def _add_device(self, dev, ip, token):
        try:
            #import importlib
            #module = importlib.import_module(".mimiio_device." + DeviceTypeDict[dev])
            _id = 'xiaomi-' + dev +token
            if _id not in self.devices:
                device = getattr(mimiio_device, DeviceTypeDict[dev])(_id, ip, token)
                self.handle_device_added(device)
        except:           
            return  

  #  def start_pairing(self, timeout):
        """
        Start the pairing process.
        timeout -- Timeout in seconds at which to quit pairing
        """

    def cancel_pairing(self):
        """Cancel the pairing process."""
        self.pairing = False
