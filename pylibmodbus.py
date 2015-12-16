from ctypes import *
from struct import pack

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


class ModbusMappingT(Structure):
    _fields_ = [
        ("nb_bits", c_int),
        ("nb_input_bits", c_int),
        ("nb_input_registers", c_int),
        ("nb_registers", c_int),
        ("tab_bits", c_uint8),
        ("tab_input_bits", c_uint8),
        ("tab_input_registers", c_uint8),
        ("tab_registers", c_uint8),
    ]


class Modbus:
    def __init__(self, path='modbus.dll'):
        self.mb = POINTER(ModbusT)
        self.libmodbus = CDLL(path, use_errno=True)
        self.mapping = None

        self.libmodbus.modbus_strerror.restype = c_char_p

    def new_tcp(self, addr, port):
        self.mb = self.libmodbus.modbus_new_tcp(addr.encode("ascii"), port)

    def new_rtu(self, dev, baud, parity, data_bit, stop_bit):
        self.mb = self.libmodbus.modbus_new_rtu(dev.encode("ascii"), baud, c_char(parity), data_bit, stop_bit)

    def set_slave(self, addr):
        self.libmodbus.modbus_set_slave(self.mb, addr)

    def connect(self):
        self.libmodbus.modbus_connect(self.mb)

    def read_registers(self, adr, count):
        r = create_unicode_buffer("", count)
        if self.libmodbus.modbus_read_registers(self.mb, adr, count, r) == -1:
            raise ModbusException(self.strerror())
        return list(r)

    def write_register(self, addr, value):
        self.libmodbus.modbus_write_register(self.mb, addr, value)

    def write_registers(self, addr, values):
        l = len(values)
        if self.libmodbus.modbus_write_registers(self.mb, addr, l, pack("H" * l, *values)) == -1:
            raise ModbusException(self.strerror())

    def close(self):
        self.libmodbus.modbus_close(self.mb)
        self.libmodbus.modbus_free(self.mb)

    def mapping_new(self, nb_bits, nb_input_bits, nb_registers, nb_input_registers):
        self.mapping = self.libmodbus.modbus_mapping_new(nb_bits, nb_input_bits, nb_registers, nb_input_registers)

    def mapping_free(self):
        self.libmodbus.modbus_mapping_free(POINTER(self.mapping))

    def receve(self):
        req = POINTER(c_uint8)
        length = self.libmodbus.modbus_receive(self.mb, req)
        print("receve:", length, req)
        return length, req

    def reply(self, req_len):
        req = POINTER(c_uint8)
        length = self.libmodbus.modbus_reply(self.mb, req, req_len, POINTER(self.mapping))
        print("reply: " + length)
        return length

    def strerror(self):
        return self.libmodbus.modbus_strerror(get_errno())

    def set_debug(self, val):
        self.libmodbus.modbus_set_debug(self.mb, val)


class ModbusException(Exception):
    pass
