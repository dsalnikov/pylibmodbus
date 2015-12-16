from pylibmodbus import *

if __name__ == "__main__":
    mb = Modbus()
    mb.new_tcp("192.168.0.5", 502)
    mb.connect()
    try:
        resp = mb.read_registers(200, 5)
        print resp
    except ModbusException, msg:
        print "Modbus error:", msg
    mb.close()
