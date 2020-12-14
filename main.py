#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.label import Label

import gattlib.adapter
import gattlib.device

import sys
import time

from android.permissions import request_permissions, Permission

class MyApp(App):

    def build(self):
        adapter = gattlib.adapter.Adapter()
        adapter.open()
        scanned_device = None
        def on_scan(device, userdata):
            nonlocal scanned_device
            print(device)
            scanned_device = device
        adapter.scan_enable(on_scan, 10)
        if scanned_device is None:
            print('no devices found yet')
            return Label(text = 'no devices found yet')
        scanned_device.connect()
        scanned_device.discover()
        print('services', scanned_device.services)
        return Label(text = 'services\b' + '\n'.join(str(service.uuid) for service in scanned_device.services.values()))


if __name__ == '__main__':
    app = MyApp()
    app.run()
