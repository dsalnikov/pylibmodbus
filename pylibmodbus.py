from ctypes import *

FD_SETSIZE = 64
SOCKET = c_uint


class Timeval(Structure):
    _fields_ = [
        ("tv_sec", c_long),
        ("tv_usec", c_long)
    ]


class SftT(Structure):
    _fields_ = [
        ("slave", c_int),
        ("fubction", c_int),
        ("t_id", c_int)
    ]


class ModbusBackendT(Structure):
    pass


class ModbusT(Structure):
    _fields_ = [
        ("slave", c_int),
        ("s", c_int),
        ("debug", c_int),
        ("error_recovery", c_int),
        ("response_timeout", Timeval),
        ("byte_timeout", Timeval),
        ("backend", POINTER(ModbusBackendT)),
        ("backend_data", c_void_p)
    ]


class FdSet(Structure):
    _fields_ = [
        ("fd_count", c_uint),
        ("fd_array", SOCKET*FD_SETSIZE)
    ]

class ModbusBackendT(Structure):
    _fields_ = [
        ("backend_type", c_uint),
        ("header_length", c_uint),
        ("checksum_length", c_uint),
        ("max_adu_length", c_uint),
        ("set_slave", CFUNCTYPE(c_int, POINTER(ModbusT), c_int)),
        ("build_request_basis", CFUNCTYPE(c_int, POINTER(ModbusT), c_int, c_int, c_int, c_char_p)),
        ("build_response_basis", CFUNCTYPE(c_int, POINTER(SftT), c_char_p)),
        ("prepare_response_tid", CFUNCTYPE(c_int, c_char_p, POINTER(c_int))),
        ("send_msg_pre", CFUNCTYPE(c_int, c_char_p, c_int)),
        ("send", CFUNCTYPE(c_ssize_t, POINTER(ModbusT), c_char_p, c_int)),
        ("receive", CFUNCTYPE(c_int, POINTER(ModbusT), c_char_p)),
        ("recv", CFUNCTYPE(c_ssize_t, POINTER(ModbusT), c_char_p, c_int)),
        ("check_integrity", CFUNCTYPE(c_int, POINTER(ModbusT), c_char_p, c_int)),
        ("pre_check_confirmation", CFUNCTYPE(c_int, POINTER(ModbusT), c_char_p, c_char_p, c_int)),
        ("connect", CFUNCTYPE(c_int, POINTER(ModbusT))),
        ("close", CFUNCTYPE(None, POINTER(ModbusT))),
        ("flush", CFUNCTYPE(c_int, POINTER(ModbusT))),
        ("select", CFUNCTYPE(c_int, POINTER(ModbusT), POINTER(FdSet), POINTER(Timeval), c_int)),
        ("free", CFUNCTYPE(None, POINTER(ModbusT)))
    ]


class Modbus:
    def __init__(self):
        self.mb = POINTER(ModbusT)
        self.libmodbus = CDLL("modbus.dll")

    def new_tcp(self, addr, port):
        self.mb = self.libmodbus.modbus_new_tcp(addr.encode("ascii"), port)

    def connect(self):
        self.libmodbus.modbus_connect(self.mb)

    def read_registers(self, adr, count):
        r = create_unicode_buffer("", count)
        self.libmodbus.modbus_read_registers(self.mb, adr, count, r)
        return list(r)

    def close(self):
        self.libmodbus.modbus_close(self.mb)

    def free(self):
        self.libmodbus.modbus_free(self.mb)