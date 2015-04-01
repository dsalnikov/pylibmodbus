from pylibmodbus import *

if __name__ == "__main__":
    mb = Modbus()
    mb.new_tcp("192.168.0.5", 502)
    mb.connect()
    resp = mb.read_registers(200, 5)
    print(resp)
    mb.close()
    mb.free()