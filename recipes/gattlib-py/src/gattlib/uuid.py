import re
from uuid import UUID

SDP_UUID16 = 0x19
SDP_UUID32 = 0x1A
SDP_UUID128 = 0x1C

GATT_STANDARD_UUID_FORMAT = re.compile("(\S+)-0000-1000-8000-00805f9b34fb", flags=re.IGNORECASE)

def gattlib_uuid_to_uuid(gattlib_uuid):
    return UUID(gattlib_uuid.toString())

def gattlib_uuid_to_int(gattlib_uuid):
    return gattlib_uuid_str_to_int(gattlib_uuid.toString())

def gattlib_uuid_str_to_int(uuid_str):
    # Check if the string could already encode a UUID16 or UUID32
    if len(uuid_str) <= 8:
        return int(uuid_str, 16)

    # Check if it is a standard UUID or not
    match = GATT_STANDARD_UUID_FORMAT.search(uuid_str)
    if match:
        return int(match.group(1), 16)
    else:
        return UUID(uuid_str).int
