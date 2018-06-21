from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from decimal import Decimal
import decimal
import json
import struct
import time

#TODO has not been tested need to test on instrumennt and fix

class generic_driver_pymodbus(ModbusClient):
    def __init__(self,spec):
        self.spec = spec
        self.address = spec['address']
        self.operations = spec['operations']
        ModbusClient.__init__(self,method='rtu', port=spec['port'], timeout=1, baudrate=spec['baudrate'])
        self.store = {}
        self.timeout = 2

    def read_instrument(self,op_id):
        op = self.operations[op_id]
        stored = self.store.get(op_id, (None, time.time() - (self.timeout + 1)))
        if time.time() - stored[1] < self.timeout:
            data ,data_trans = stored[0]
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
            data = self.decimals(data,op)
            data_trans = self.transform(data,op)
            self.close()
            self.store[op_id] = ((data,data_trans), time.time())
        return data, data_trans

    def decimals(self,data,operation):
        d_shift = operation.get('decimal_shift',0)
        return Decimal(data).scaleb(d_shift)

    def transform(self,data,operation):
        x = data
        eq = operation.get("transform_eq",'x')
        c = operation.get("transform_coeff",None)
        result = eval(eq)
        return result


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

    print(instr.read_instrument('read_rh'))
    print(instr.read_instrument('read_dewpoint'))
    print(instr.read_instrument('read_pressure'))


if __name__ == '__main__':
    main()