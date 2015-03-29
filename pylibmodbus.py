from ctypes import *

class timeval(Structure):
    _fields_ = [
        ("tv_sec", c_long),
        ("tv_usec",c_long)
    ]

class sft_t(Structure):
    _fields_ = [
        ("slave", c_int),
        ("fubction", c_int),
        ("t_id", c_int)
    ]

class modbus_backend_t(Structure):
    pass

class modbus_t(Structure):
    _fields_ = [
        ("slave", c_int),
        ("s", c_int),
        ("debug", c_int),
        ("error_recovery", c_int),
        ("response_timeout", timeval),
        ("byte_timeout", timeval),
        ("backend", POINTER(modbus_backend_t)),
        ("backend_data", c_void_p)
    ]

FD_SETSIZE = 64
SOCKET = c_uint

class fd_set(Structure):
    _fields_ = [
        ("fd_count", c_uint),
        ("fd_array", SOCKET*FD_SETSIZE)
    ]

class modbus_backend_t(Structure):
    _fields_ = [
        ("backend_type", c_uint),
        ("header_length", c_uint),
        ("checksum_length", c_uint),
        ("max_adu_length", c_uint),
        ("set_slave", CFUNCTYPE(c_int, POINTER(modbus_t), c_int)),
        ("build_request_basis", CFUNCTYPE(c_int, POINTER(modbus_t), c_int, c_int, c_int, c_char_p)),
        ("build_response_basis", CFUNCTYPE(c_int, POINTER(sft_t), c_char_p)),
        ("prepare_response_tid", CFUNCTYPE(c_int, c_char_p, POINTER(c_int))),
        ("send_msg_pre", CFUNCTYPE(c_int, c_char_p, c_int)),
        ("send", CFUNCTYPE(c_ssize_t, POINTER(modbus_t), c_char_p, c_int)),
        ("receive", CFUNCTYPE(c_int, POINTER(modbus_t), c_char_p)),
        ("recv", CFUNCTYPE(c_ssize_t, POINTER(modbus_t), c_char_p, c_int)),
        ("check_integrity", CFUNCTYPE(c_int, POINTER(modbus_t), c_char_p, c_int)),
        ("pre_check_confirmation", CFUNCTYPE(c_int, POINTER(modbus_t), c_char_p, c_char_p, c_int)),
        ("connect", CFUNCTYPE(c_int, POINTER(modbus_t))),
        ("close", CFUNCTYPE(None, POINTER(modbus_t))),
        ("flush", CFUNCTYPE(c_int, POINTER(modbus_t))),
        ("select", CFUNCTYPE(c_int, POINTER(modbus_t), POINTER(fd_set), POINTER(timeval), c_int)),
        ("free", CFUNCTYPE(None, POINTER(modbus_t)))
    ]


