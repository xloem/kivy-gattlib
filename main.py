#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label

print('Debug')

import gattlib.adapter
import gattlib.device

import sys
import time

from android.permissions import request_permissions, Permission

class MyApp(App):

    def build(self):
        adapter = gattlib.adapter.Adapter()
        adapter.open()
        scanned_devices = []
        def on_scan(device, userdata):
            nonlocal scanned_device
            print(device)
            scanned_devices.append(device)
        adapter.scan_enable(on_scan, 5)
        if len(scanned_devices) == 0:
            print('no devices found yet')
            return Label(text = 'no devices found yet')
        summary = ''
        for scanned_device in scanned_devices:
            summary += str(scanned_device) + ':\n'
            scanned_device.connect()
            scanned_device.discover()
            for service in scanned_device.services.values():
                summary += '  service ' + str(service.uuid) + '\n'
            for characteristic in scanned_device.characteristics.values():
                summary += '  characteristic ' + str(characteristic.uuid) + '\n'
            print(summary)
        return Label(text = summary, font_size='10sp')


if __name__ == '__main__':
    app = MyApp()
    app.run()
