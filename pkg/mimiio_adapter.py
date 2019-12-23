"""mimiio adapter for Mozilla WebThings Gateway."""

from gateway_addon import Adapter, Database
import pkg.mimiio_device 


_TIMEOUT = 3

DeviceTypeDict = {
    'PhilipsZhiruiSmartLEDBulb': 'PhilipsBulb',
    'XiaomiMiRobotVacuum': 'Vacuum',
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
        #self.add_from_config()
        self.start_pairing(_TIMEOUT)

    def add_from_config(self):
        """Attempt to add all configured devices."""
        database = Database(self.package_name)
        if database.open():
            config = database.load_config()            
            if not config or 'Token' not in config or 'IPaddress' not in config:
                return
            if (config['Token'] is not '') and (config['IPaddress'] is not ''):
                self._add_device(config['DeviceType'], config['IPaddress'],config['Token'] )
                #print("add"+ str(config['DeviceType'])+ str(config['Token']))
            database.close() 
    def _add_device(self, dev, ip, token):
        try:
            _id = 'xiaomi-' + dev +token
            if _id not in self.devices:
                #print("token：" +token)
                #print("ip："+ip)
                device = getattr(pkg.mimiio_device, DeviceTypeDict[dev])(self, _id, ip, token)
                self.handle_device_added(device)
            else:
                print("device already in system")
        except:
            print("failed to add new device...")


    def start_pairing(self, timeout):
        """
        Start the pairing process.
        timeout -- Timeout in seconds at which to quit pairing
        """
        if self.pairing:
            return

        self.pairing = True
        self.add_from_config()
        self.pairing = False
        

    def cancel_pairing(self):
        """Cancel the pairing process."""
        self.pairing = False
