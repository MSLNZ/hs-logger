import visa
import json
import time

class generic_driver_visa(object):

    def __init__(self, spec):
        #self.spec = json.load(spec)
        #print(spec)
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
        stored = self.store.get('operation_id',(none,0))
        if time.time() - stored[2]>= self.timeout:
           result =  stored[1]
        else:
            result = self.instrument.query(operation['command'])
            self.store[operation_id] = (result,time.time())
        return result

    #todo writing to instruments
    def write_instrument(self,operation_id,values):
        """
        write instrument 
        """
        return "not working yet"


#testing
def main():
    instr = generic_driver_visa(json.load(open('../instruments/LHG3900_visa.json')))
    print (instr.read_instrument('read_default'))

if __name__ == '__main__':
    main()