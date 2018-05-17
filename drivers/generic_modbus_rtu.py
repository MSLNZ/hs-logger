import minimalmodbus
import struct
import time
import json

# older version using minimalmodbus use only for reference dose not function correctly

class generic_modbus_rtu(minimalmodbus.Instrument):

    def __init__(self,spec):
        self.spec = spec
        self.op_list = spec["operations"]

        minimalmodbus.Instrument.__init__(self,spec["port"],spec["address"])
        self.serial.baudrate = spec["baudrate"]
        self.serial.bytesize = spec["databits"]
        self.serial.stopbits = spec["stopbits"]
        self.serial.close()
        self.serial.open()
        self.update_on_request = True
        self.update_expire_time = spec["update_time"]
        self.data_registers = spec["data_registers"]
        self.raw_data = {}
        self.update_all()
        self.last_update = time.time()


    def update_all(self):
        for start,end in self.data_registers:
            print(start,end)
            count = end-start
            data_list = self.read_registers(start,count)
            indexs = list(range(start,end))
            self.raw_data.update(zip(indexs,data_list))

    def get_value(self,operation_id):
        if self.update_on_request:
            if time.time() - self.last_update >= self.update_expire_time :
                self.update_all()
                self.last_update = time.time()
        op = self.op_list.get(operation_id)
        reg = op.get('register')
        datatype = op.get('data_type')
        #conversion = getattr(self,'_to_{}'.format(datatype))
        conversion = self.uint_conversion(datatype)
        data = conversion(reg)
        return data

    def get_data(self,operation_ids):
        data = {}
        if isinstance(operation_ids,str):
            data[operation_ids] = self.get_value(operation_ids)
        else:
            for op_id in operation_ids:
                data[op_id] = self.get_value(op_id)
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
            return self.uint_to_uint


    def uint_to_float(self, index):
       mp = struct.pack('!HH',self.raw_data.get(index),self.raw_data.get(index+1))
       return struct.unpack('!f',mp)[0]

    def uint_to_int(self, index):
       mp = struct.pack('!H', self.raw_data.get(index))
       return struct.unpack('!h', mp)[0]

    def uint_to_uint(self, index):
       return self.raw_data.get(index)

    def _to_uint(self, index):
       mp = struct.pack('!H', self.raw_data.get(index))
       return struct.unpack('!h', mp)[0]
#jls CHANGED BIG-ENDIAN ! above TO little-endian < below

    # def uint_to_float(self, index):
    #     mp = struct.pack('<HH',self.raw_data.get(index),self.raw_data.get(index+1))
    #     return struct.unpack('<f',mp)[0]
    #
    # def uint_to_int(self,index):
    #     mp = struct.pack('<H',self.raw_data.get(index))
    #     return  struct.unpack('<h',mp)[0]
    #
    # def uint_to_uint(self,index):
    #     return  self.raw_data.get(index)
    #
    # def _to_uint(self,index):
    #     mp = struct.pack('<H',self.raw_data.get(index))
    #     return  struct.unpack('<h',mp)[0]
