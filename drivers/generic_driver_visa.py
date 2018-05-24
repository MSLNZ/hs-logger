import visa
import json
import time
from decimal import Decimal

class generic_driver_visa(object):

    def __init__(self, spec):

        self.operations = spec['operations']
        port = spec["port"]
        baud = spec["baudrate"]
        w_term = spec["write_termination"]
        r_term = spec["read_termination"]
        rm = visa.ResourceManager()
        self.store = {}
        self.timeout = 2
        self.instrument = rm.open_resource(port,
                                           baud_rate=baud,
                                           write_termination=w_term,
                                           read_termination=r_term)
        self.instrument.open()

    def read_instrument(self,operation_id):
        """
        read instrument 
        """
        operation = self.operations[operation_id]
        datatype = operation['data_type']
        type = operation['type']
        stored = self.store.get(operation_id,(None,time.time()-(self.timeout+1)))
        if time.time() - stored[1]< self.timeout:
           data,data_trans = stored[0]
           print("using stored") #testing
        else:
            data = self.instrument.query(operation['command'])
            if type == 'read_multiple':
                data = data.split(operation.get("split"))
                data = [self.decimals(d,operation) for d in data]
                data_trans = [self.transform(d, operation) for d in data]
            else:
                data = self.decimals(data,operation)
                data_trans = self.transform(data, operation)

            self.store[operation_id] = ((data,data_trans),time.time())

        return data, data_trans

    #todo writing to instruments
    def write_instrument(self,operation_id,values):
        """
        write instrument 
        """
        return "not working yet"

    def decimals(self,data,operation):
        d_shift = operation.get('decimal_shift',0)
        return Decimal(data).scaleb(d_shift)

    def transform(self,data,operation):
        x = data
        eq = operation.get("transform_eq",'x')
        c = operation.get("transform_coeff",None)
        result = eval(eq)
        return result

    def convert_to(self,data,datatype):
        if datatype == 'int':
            return int(data)
        elif datatype == 'float':
            return float(data)
        else:
            return data

#testing
def main():
    instr = generic_driver_visa(json.load(open('../instruments/LHG3900_visa.json')))
    print (instr.read_instrument('read_default'))
    print (instr.read_instrument('read_default'))
    time.sleep(2)
    print (instr.read_instrument('read_default'))


if __name__ == '__main__':
    main()