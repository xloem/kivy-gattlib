from .device import Device
from .exception import *

from jnius import autoclass, cast, PythonJavaClass, java_method, JavaClass, MetaJavaClass
import concurrent.futures 

from android.permissions import request_permissions, Permission
import time

_BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
_ScanCallback = autoclass('android.bluetooth.le.ScanCallback')
_ScanFilter = autoclass('android.bluetooth.le.ScanFilter')
_ScanSettings = autoclass('android.bluetooth.le.ScanSettings')
_ScanSettingsBuilder = autoclass('android.bluetooth.le.ScanSettings$Builder')
_List = autoclass('java.util.ArrayList')
_PythonScanCallback = autoclass('PythonScanCallback')

class Adapter:

    def __init__(self, name=None):
        self._name = name
        self._adapter = None
        self._is_opened = False

    @staticmethod
    def list():
        raise NotImplementedError("this is unimplemented in core gattlib as of 2020-12")

    def open(self):
        self._adapter = _BluetoothAdapter.getDefaultAdapter()
        self._is_opened = True

    def close(self):
        self._adapter = None
        self._is_opened = False

    def scan_enable(self, on_discovered_device_callback, timeout, notify_change=False, uuids=None, rssi_threshold=None, user_data=None):

        if not self._is_opened:
            raise AdapterNotOpened()

        permission_acknowledged = concurrent.futures.Future()
        def handle_permissions(permissions, grantResults):
            if any(grantResults):
                permission_acknowledged.set_result(grantResults)
            else:
                permission_acknowledged.set_exception(DeviceError("User denied access to " + str(permissions)))
        request_permissions([Permission.ACCESS_FINE_LOCATION,Permission.ACCESS_COARSE_LOCATION,'android.permission.ACCESS_BACKGROUND_LOCATION'], handle_permissions)
        permission_acknowledged.result()

        start_time = time.monotonic()
        end_time = start_time + timeout

        callback = PythonScanCallback()
        result = callback.scanResult
        androidcallback = _PythonScanCallback(callback)

        scanner = self._adapter.getBluetoothLeScanner()
        #callback.startScan()
        scanner.startScan(cast('java.util.List',_List()), _ScanSettingsBuilder().setScanMode(_ScanSettings.SCAN_MODE_LOW_LATENCY).setReportDelay(0).setPhy(_ScanSettings.PHY_LE_ALL_SUPPORTED).setNumOfMatches(_ScanSettings.MATCH_NUM_MAX_ADVERTISEMENT).setMatchMode(_ScanSettings.MATCH_MODE_AGGRESSIVE).setCallbackType(_ScanSettings.CALLBACK_TYPE_ALL_MATCHES).build(), androidcallback)
        addrs_seen = set()
        while True:
            now = time.monotonic()
            if now > end_time:
                break
            try:
                scanResult, result = result.result(end_time - time.monotonic())
            except concurrent.futures.TimeoutError:
                break
            androidDevice = scanResult.getDevice()
            addr = androidDevice.getAddress()
            if addr in addrs_seen:
                continue
            addrs_seen.add(addr)
            device = Device(self, addr, androidDevice.getAlias())
            on_discovered_device_callback(device, user_data)
        scanner.stopScan(androidcallback)

    def get_rssi_from_mac(self, mac_address):
        raise NotImplementedError()

class PythonAbstractScanCallback(JavaClass, metaclass=MetaJavaClass):
    __javaclass__ = 'android/bluetooth/le/ScanCallback'

    # this approach could work
    # but i think it's just a copy of autoclass

class PythonScanCallback(PythonJavaClass):
    __javainterfaces__ = ['PythonScanCallback$Interface']
    __javacontext__ = 'app'

    _errors = {
        _ScanCallback.SCAN_FAILED_ALREADY_STARTED: InvalidParameter,
        _ScanCallback.SCAN_FAILED_APPLICATION_REGISTRATION_FAILED: DBusError,
        _ScanCallback.SCAN_FAILED_FEATURE_UNSUPPORTED: NotSupported,
        _ScanCallback.SCAN_FAILED_INTERNAL_ERROR: DeviceError
    }

    def __init__(self):
        self.scanResult = concurrent.futures.Future()

    @java_method('(I)V')
    def onScanFailed(self, errorCode):
        self.scanResult.set_exception(self._errors[errorCode]())

    @java_method('(Landroid/bluetooth/le/ScanResult;)V')
    def onScanResult(self, result):
        next = concurrent.futures.Future()
        self.scanResult.set_result((result, next))
        self.scanResult = next
