import serial
import json
import time
import numpy as np
import math
import re

from threading import Lock

class generic_driver_py_serial(object):

    def __init__(self, spec):
        self.spec = spec
        self.operations = spec['operations']
        port = spec["port"]
        baud = spec["baudrate"]
        par = spec["parity"]
        stop_B = spec["stopbits"]
        time_out = spec["timeout"]
        self.w_term = spec.get("write_termination", '\r')
        self.r_term = spec.get("read_termination", '\r')

        self.store = {}
        self.timeout = spec.get("store_timeout", 2)

        # self.instrument = serial.Serial('COM6',
        #                                 19200,
        #                                 parity=serial.PARITY_NONE,
        #                                 stopbits=serial.STOPBITS_ONE,
        #                                 timeout=3)

        self.instrument = serial.Serial(port,
                                        baud,
                                        timeout=time_out)

        if par == "odd":
            self.instrument.parity = serial.PARITY_ODD
        elif par == "even":
            self.instrument.parity = serial.PARITY_EVEN
        elif par == "mark":
            self.instrument.parity = serial.PARITY_MARK
        elif par == "space":
            self.instrument.parity = serial.PARITY_SPACE
        else:
            self.instrument.parity = serial.PARITY_NONE

        if par == "2":
            self.instrument.stopbits = serial.STOPBITS_TWO
        elif par == "1.5":
            self.instrument.stopbits = serial.STOPBITS_ONE_POINT_FIVE
        else:
            self.instrument.stopbits = serial.STOPBITS_ONE

        self.lock = Lock()
        


    def read_instrument(self, operation_id):
        """
        read instrument
        """
        operation = self.operations[operation_id]
        # datatype = operation['data_type']
        type = operation['type']
        echo = self.spec.get('echo', False)

        stored = self.store.get(operation_id, (None, time.time() - (self.timeout + 1))) #what is this?

        if time.time() - stored[1] < self.timeout:
            data, data_trans = stored[0]
        else:
            if type == 'read_single':
                with self.lock:
                    # print("locK")
                    cmd_e = (operation['command']).encode("ascii") + self.w_term.encode("ascii")
                    self.instrument.write(cmd_e)
                    data = self.instrument.read_until(self.r_term)
                    floats_data = re.findall(r"[-+]?\d*\.\d+|\d+", str(data))
                    data = float(floats_data[0])

                    data_trans = self.transform(data, operation)
                # print('unlocK')
            else:
                with self.lock:
                    # print("lock")
                    print(operation['command'])
                    cmd_e = (operation['command']).encode("ascii") + self.w_term.encode("ascii")
                    self.instrument.write(cmd_e)
                    data = str(self.instrument.read_until(self.r_term))
                    print(data)

                    data = []
                    data_trans = []
                # print('unlock')
            self.store[operation_id] = ((data, data_trans), time.time())

        return data, data_trans

    def write_instrument(self, operation_id, values):
        with self.lock:
            """
            write instrument 
            """
            # todo: check valid values for sending to instrument
            op = self.operations[operation_id]
            command = op.get("command", "")
            # command = command.format(*values)
            command = command.format(*values)

            # response = self.instrument.query(command)
            cmd_e = command.encode("ascii")+self.w_term.encode("ascii")
            self.instrument.write(cmd_e)

            response = str(self.instrument.read_until(self.r_term))

            if response != "":
                print(response)
            else:
                print("No response")
            return response

    def transform(self, data, operation):
        x = data
        eq = operation.get("transform_eq", ['V', 0, 1, 0, 0])
        if self.isfloat(data):  # Check that the data can be transformed
            if eq[0] == 'T':  # Callendar-Van Dusen equation
                if np.isnan(eq[1:4]).any() or np.isinf(eq[1:4]).any() or np.isnan(x) or np.isinf(x):
                    print("{} with transform {} is out of range.".format(x, eq))
                    transformed = float("NaN")
                else:
                    fulltransformed = np.roots([eq[3], -100 * eq[3], eq[2], eq[1], (1 - (x / eq[4]))])
                    transformed = float("inf")  # Create a maximum value
                    for j in fulltransformed:
                        if np.imag(j) == 0:  # Remove imaginary roots
                            if abs(j) < transformed:
                                transformed = np.real(j)  # Find most reasonable real root
                            elif abs(j) == transformed and j > transformed:
                                transformed = np.real(j)  # If the roots are same magnitude, give positive root
                    if math.isinf(transformed):
                        print("Invalid Callendar–Van Dusen equation: No real solutions for")
                        print("R = {}, R0 = {}, A = {}, B = {}, C = {}".format(x, eq[4], eq[1], eq[2], eq[3]))
                        transformed = float("NaN")
            elif eq[0] == 'V' or eq[0] == 'P':
                transformed = eq[1] + eq[2] * x + eq[3] * x ** 2 + eq[
                    4] * x ** 3  # V and P both use cubic equations. P is
                # listed purely for record keeping purposes
            else:
                print("Transform form not recognised: {}".format(eq[0]))
                transformed = float("NaN")
        else:
            print("{} can't be transformed.".format(x))
            transformed = float("NaN")  # The data can't be transformed
        # c = operation.get("transform_coeff", None)
        # transformed = eval(eq)
        return transformed

    def convert_to(self, data, datatype):
        if datatype == 'int':
            return int(data)
        elif datatype == 'float':
            return float(data)
        else:
            return data

    def isfloat(self, data):
        try:
            float(data)  # Checks if the string can be made into a float.
            return True
        except ValueError:
            return False
# testing
def main():
    instr = generic_driver_py_serial(json.load(open('../instruments/PC200_serial.json')))
    #print(instr.read_instrument('read_Tm'))
    print(instr.write_instrument('SS',5))


if __name__ == '__main__':
    main()