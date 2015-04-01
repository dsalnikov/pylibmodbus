from ctypes import *
from pylibmodbus import *


class Modbus:
    def __init__(self):
        self.mb = POINTER(modbus_t)
        self.libmodbus = CDLL("modbus.dll")
        # TODO: move this to another method
        self.mb = self.libmodbus.modbus_new_tcp("192.168.0.5".encode("ascii"), 502)

    def connect(self):
        self.libmodbus.modbus_connect(self.mb)

    def read_registers(self,adr,count):
        r = create_unicode_buffer("", count)
        self.libmodbus.modbus_read_registers(mb, adr, count, r)
        return list(r)


if __name__ == "__main__":
    mb = POINTER(modbus_t)
    tab_reg = c_ushort * 32
    r = create_unicode_buffer("", 32)

    libmodbus = CDLL("modbus.dll")
    mb = libmodbus.modbus_new_tcp("192.168.0.5".encode("ascii"), 502)
    libmodbus.modbus_connect(mb)
    libmodbus.modbus_read_registers(mb, 0, 5, r)

    for o in r:
        print(ord(o))

    libmodbus.modbus_close(mb)
    libmodbus.modbus_free(mb)