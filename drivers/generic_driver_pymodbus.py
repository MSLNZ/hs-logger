from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import json

#TODO has not been tested need to test on instrumennt and fix

class generic_driver_pymodbus(ModbusClient):
    def __init__(self,spec):
        spec = json.load(spec)
        self.address = spec['address']
        self.operations = spec['operarions']
        ModbusClient.__init__(self,method='rtu', port=spec['port'], timeout=1, baudrate=spec['baudrate'])
        self.connect()

    def read_instrument(self,op_id):
        op = self.operations[op_id]
        op['register']
        op.get('datatype','uint')
        rr = self.read_holding_registers(op['register'], op['num_reg'], unit=self.address)
        return rr.registers

    def uint_conversion(self, datatype):
        dt = datatype.lower()
        if dt == "float":
            return self.uint_to_float
        elif dt == "int":
            return self.uint_to_int
        elif dt == "uint":
            return self.uint_to_uint
        else:
            return self.uint_to_uint

    def uint_to_float(self, index):
        mp = struct.pack('!HH', self.raw_data.get(index), self.raw_data.get(index + 1))
        return struct.unpack('!f', mp)[0]

    def uint_to_int(self, index):
        mp = struct.pack('!H', self.raw_data.get(index))
        return struct.unpack('!h', mp)[0]

    def uint_to_uint(self, index):
        return self.raw_data.get(index)

    def _to_uint(self, index):
        mp = struct.pack('!H', self.raw_data.get(index))
        return struct.unpack('!h', mp)[0]