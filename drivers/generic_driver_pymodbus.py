from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import json
import struct
import time

#TODO has not been tested need to test on instrumennt and fix

class generic_driver_pymodbus(ModbusClient):
    def __init__(self,spec):
        self.address = spec['address']
        self.operations = spec['operations']
        ModbusClient.__init__(self,method='rtu', port=spec['port'], timeout=1, baudrate=spec['baudrate'])
        self.store = {}
        self.timeout = 2

    def read_instrument(self,op_id):
        op = self.operations[op_id]
        stored = self.store.get(op_id, (None, time.time() - (self.timeout + 1)))
        if time.time() - stored[1] < self.timeout:
            data = stored[0]
        else:
            self.connect()
            converter = self.uint_conversion(op.get('data_type','uint'))
            rr = self.read_holding_registers(op['register'], op['num_reg'], unit=self.address)
            retry = 0
            while rr.isError():
                retry += 1
                print("modbus error retying {}".format(retry))
                rr = self.read_holding_registers(op['register'], op['num_reg'], unit=self.address)
                time.sleep(.2)
                if retry >= 10:
                    print("Modbus operation {} failed".format(op.get('id','')))
                    return 'error'
            data = converter(rr.registers)
            self.close()
            self.store[op_id] = (data, time.time())
        return data

    def uint_conversion(self, datatype):
        dt = datatype.lower()
        if dt == "float":
            return self.uint_to_float
        elif dt == "int":
            return self.uint_to_int
        elif dt == "uint":
            return self.uint_to_uint
        else:
            return self.to_uint

    def uint_to_float(self, data):
        mp = struct.pack('!HH', data[0], data[1])
        return struct.unpack('!f', mp)[0]

    def uint_to_int(self, data):
        mp = struct.pack('!H', data[0])
        return struct.unpack('!h', mp)[0]

    def uint_to_uint(self, data):
        return data[0]

    def to_uint(self, data):
        return data

#testing
def main():
    instr = generic_driver_pymodbus(json.load(open('../instruments/Michell_S8000rs_modbus.json')))

    print(instr.read_instrument('read_group_1'))



if __name__ == '__main__':
    main()