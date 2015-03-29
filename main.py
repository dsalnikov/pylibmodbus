from ctypes import *
from pylibmodbus import *

if __name__ == "__main__":
    mb = POINTER(modbus_t)
    tab_reg = c_ushort * 32
    r = create_unicode_buffer("", 32)

    libmodbus = CDLL("modbus.dll")
    mb = libmodbus.modbus_new_tcp("192.168.0.5".encode("ascii"),502)
    libmodbus.modbus_connect(mb)
    libmodbus.modbus_read_registers(mb,0,5,r)

    for o in r:
        print(ord(o))

    libmodbus.modbus_close(mb)
    libmodbus.modbus_free(mb)