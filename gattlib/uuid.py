from uuid import UUID

import gattlib.orig.uuid as _uuid
from gattlib.orig.uuid import (
    UUID,
    SDP_UUID16,
    SDP_UUID32,
    SDP_UUID128,
    GATT_STANDARD_UUID_FORMAT,
    gattlib_uuid_str_to_int
    )

def gattlib_uuid_to_uuid(gattlib_uuid):
    return UUID(gattlib_uuid.toString())

def gattlib_uuid_to_int(gattlib_uuid):
    return gattlib_uuid_str_to_int(gattlib_uuid.toString())
