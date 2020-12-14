
from .uuid import gattlib_uuid_to_uuid, gattlib_uuid_to_int

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
