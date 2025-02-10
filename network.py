from nmap import PortScanner, PortScannerError

class Network(object):
    def __init__(self, ip=None):
        self.ip_default = '192.168.1.1'
        self.ip = ip if ip else self.ip_default

    def get_devices(self):
        """Return a list of devices with additional details."""
        network_to_scan = self.ip + '/24'  # Adjust the subnet mask as necessary

        p_scanner = PortScanner()
        try:
            print('Scanning {}...'.format(network_to_scan))
            p_scanner.scan(hosts=network_to_scan, arguments='-sn')  # '-sn' for ping scan, no port scan
        except PortScannerError as e:
            print(f"Scan error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

        device_list = []
        for device in p_scanner.all_hosts():
            if p_scanner[device].state() == 'up':
                info = p_scanner[device]
                device_data = {
                    'host': device,
                    'mac': info['addresses'].get('mac', 'UNKNOWN_MAC'),
                    'model_name': 'Unknown',
                    'os': 'Unknown',
                    'hostnames': info['hostnames'],
                }
                device_list.append((device, device_data))

        return device_list

# Update the GUI and main class as necessary to handle the modified Network class.
