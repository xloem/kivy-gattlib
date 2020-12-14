
from jnius import autoclass, PythonJavaClass, java_method

from .uuid import gattlib_uuid_to_uuid, gattlib_uuid_to_int

_BluetoothGattCharacteristic = autoclass('android.bluetooth.BluetoothGattCharacteristic')

class GattService():

    def __init__(self, device, gattlib_primary_service):
        self._device = device
        self._gattlib_primary_service = gattlib_primary_service
    
    @property
    def uuid(self):
        return gattlib_uuid_to_uuid(self._gattlib_primary_service.getUuid())

    @property
    def short_uuid(self):
        return gattlib_uuid_to_int(self._gattlib_primary_service.getUuid())

class GattCharacteristic():

    def __init__(self, device, gattlib_characteristic):
        self._device = device
        self._gattlib_characteristic = gattlib_characteristic

    @property
    def uuid(self):
        return gattlib_uuid_to_uuid(self._gattlib_characteristic.getUuid())

    @property
    def short_uuid(self):
        return gattlib_uuid_to_int(self._gattlib_characteristic.getUuid())
        

    def write(self, data, without_response=False):
        if not isinstance(data, bytes) and not isinstance(data, bytearray):
            raise TypeError('Data must be of bytes type to know its size.')

        if without_response:
            self._gattlib_characteristic.setWriteType(_BluetoothGattCharacteristic.WRITE_TYPE_NO_RESPONSE)
        else:
            self._gattlib_characteristic.setWriteType(_BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT)
        self._gattlib_characteristic.setValue(data)

        device._callback.reset()
        device._device.writeCharacteristic(self._gattlib_characteristic)        
        device._wait()

    def register_notification(self, callback, user_data = None):
    
        class Handler(PythonJavaClass):
            __javainterface__ = ['java.lang.Runnable']
            def __init__(self, characteristic, callback, user_data):
                self.characteristic = characteristic._gattlib_characteristic
                self.callback = callback
                self.user_data = user_data
            @java_method('()V')
            def run(self):
                self.callback(self.characteristic.getValue(), self.user_data)

        self._device._callback.subscribe(self._characteristic.getUuid(), Handler())
        

    def notification_start(self):
        success = device._device.setCharacteristicNotification(self._gattlib_characteristic, True)
        if not success:
            raise DeviceError()

    def notification_stop(self):
        success = device._device.setCharacteristicNotification(self._gattlib_characteristic, False)
        if not success:
            raise DeviceError()

    def __str__(self):
        return str(self.uuid)
