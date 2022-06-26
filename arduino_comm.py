
# When this script is run for the first time, it might prompt you for 
# permission. Accept the permission and run this script again, then it should 
# send the data as expected.

# Kivy is needed for pyjnius behind the scene.
import kivy
from usb4a import usb
from usbserial4a import serial4a
from pprint import pprint
from kivy.logger import Logger
from kivy.uix.label import Label


import image_processing # .debug - to add debug on mobile screen

command_dict = dict()
command_dict[b'F'] = 'FORWARD'
command_dict[b'B'] = 'BACKWARD'
command_dict[b'R'] = 'RIGHT'
command_dict[b'L'] = 'LEFT'
command_dict[b'S'] = 'STOP'
command_dict[b'K'] = 'PICK'
command_dict[b'E'] = 'PLACE'
command_dict[b'G'] = 'S_RIGHT1'
command_dict[b'T'] = 'S_LEFT1'
command_dict[b'Q'] = 'S_RIGHT2'
command_dict[b'W'] = 'S_LEFT2'
command_dict[b'Y'] = 'S_RIGHT3'
command_dict[b'U'] = 'S_LEFT3'

class Arduino_comm:
    def start_comm(self):
        self.usb_device_list = usb.get_usb_device_list()
        # image_processing.debug =  str(usb.get_usb_device_list())
        usb_device_dict = {
            device.getDeviceName():[            # Device name
                device.getVendorId(),           # Vendor ID
                device.getManufacturerName(),   # Manufacturer name
                device.getProductId(),          # Product ID
                device.getProductName()         # Product name
                ] for device in self.usb_device_list
            }
        if self.usb_device_list:
            self.serial_port = serial4a.get_serial_port(
                self.usb_device_list[0].getDeviceName(), 
                9600,   # Baudrate
                8,      # Number of data bits(5, 6, 7 or 8)
                'N',    # Parity('N', 'E', 'O', 'M' or 'S')
                1)      # Number of stop bits(1, 1.5 or 2)
            

    def send_date(self,char):
        image_processing.debug =  command_dict[char]
        if self.usb_device_list and self.serial_port and self.serial_port.is_open:
            self.serial_port.write(char)
        else:
            self.start_comm()
        

    def end_comm(self):
        self.serial_port.close()

        # if self.serial_port:
        #     with self.port_thread_lock:
        #         self.serial_port.close()


arduino_comm = Arduino_comm()


