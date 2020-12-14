import logging

from jnius import autoclass, cast, PythonJavaClass, java_method
from concurrent.futures import Future

from .gatt import GattService#, GattCharacteristic

from .exception import *

CONNECTION_OPTIONS_LEGACY_BDADDR_LE_PUBLIC = (1 << 0)
CONNECTION_OPTIONS_LEGACY_BDADDR_LE_RANDOM = (1 << 1)
CONNECTION_OPTIONS_LEGACY_BT_SEC_LOW = (1 << 2)
CONNECTION_OPTIONS_LEGACY_BT_SEC_MEDIUM = (1 << 3)
CONNECTION_OPTIONS_LEGACY_BT_SEC_HIGH = (1 << 4)

CONNECTION_OPTIONS_LEGACY_DEFAULT = \
        CONNECTION_OPTIONS_LEGACY_BDADDR_LE_PUBLIC | \
        CONNECTION_OPTIONS_LEGACY_BDADDR_LE_RANDOM | \
        CONNECTION_OPTIONS_LEGACY_BT_SEC_LOW

_BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
_BluetoothGatt = autoclass('android.bluetooth.BluetoothGatt')
_BluetoothProfile = autoclass('android.bluetooth.BluetoothProfile')
_PythonActivity = autoclass('org.kivy.android.PythonActivity')
_PythonBluetoothGattCallback = autoclass('PythonBluetoothGattCallback')
_ExecutionException = autoclass('java.util.concurrent.ExecutionException')

class Device:

    def __init__(self, adapter, addr, name=None):
        self._adapter = adapter
        if type(addr) == str:
            addr = addr.encode("utf-8")
        self._addr = addr
        self._name = name
        self._connection = None

        self._device = self._adapter._adapter.getRemoteDevice(self.id)

        # Keep track if notificaiton handler has been initialized
        self._is_notification_init = False

        # Dictionnary for GATT characteristic callback
        self._gatt_characteristic_callbacks = {}

    @property
    def id(self):
        return self._addr.decode("utf-8")

    @property
    def connection(self):
        return self._connection

    def _wait(self):
        try:
            return self._callback.waitFor()
        except _ExecutionException as e:
            raise DeviceError(e.getCause().getMessage())

    def connect(self, options=CONNECTION_OPTIONS_LEGACY_DEFAULT):
        currentActivity = cast('android.app.Activity', _PythonActivity.mActivity)
        context = cast('android.content.Context', currentActivity.getApplicationContext())
        self._callback = _PythonBluetoothGattCallback()#PythonGattCallback()
        self._device.connectGatt(context, False, self._callback)
        self._connection = self._wait()

    def discover(self):
        #
        # Discover GATT Services
        #

        self._callback.reset()
        if not self._connection.discoverServices():
            raise DeviceError("failed to initiate service discovery")
        self._wait()

        _services = self._connection.getServices()

        self._services = {}
        for i in range(len(_services)):
            service = GattService(self, _services[i])
            self._services[service.short_uuid] = service

            logging.debug("Service UUID:0x%x" % service.short_uuid)

        #
        # Discover GATT Characteristics
        #
        
        for service in self._services.values():
            for characteristic in service.gattlib_primary_service.getCharacteristics():
                print(characteristic.getUuid().toString())

#class PythonGattCallback(PythonJavaClass):
#    __javainterfaces__ = ['android.bluetooth.BluetoothGattCallback']
#
#    def __init__(self):
#        self.connecting = Future()
#
#    @java_method('(Landroid.bluetooth.BluetoothGattII)')
#    def onConnectionStateChange(self, gatt, status, newState):
#        if newState == _BluetoothProfile.STATE_CONNECTED:
#            if status == _BluetoothGatt.GATT_SUCCESS:
#                self.connecting.set_result(gatt)
#        else: # disconnected
#            if status != _BluetoothGatt.GATT_SUCCESS:
#                self.connecting.set_exception(DeviceError(status))
#
#    @java_method('(Landroid.bluetooth.BluetoothGattI)')
#    def onServicesDiscovered(self, gatt, status):
#        if status == _BluetoothGatt.GATT_SUCCESS:
#            gatt.futureServicesDiscovered.set_result()
#        else:
#            gatt.futureServicesDiscovered.set_exception(DeviceError(status))
#
#    
