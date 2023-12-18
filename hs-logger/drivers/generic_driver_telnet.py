import pyvisa as visa
import telnetlib
import serial
import json
import time
from decimal import Decimal
from threading import Lock
import numpy as np
import math
import re


class generic_driver_telnet(object):

    def __init__(self, spec):
        """This driver expects to receive information on:
        port, baud rate, read/write terms
        It can also accept doOpen = False, which will skip the open instrument command"""
        self.spec = spec
        self.operations = spec.get('operations', {})
        self.host = spec.get('host', '10.12.97.7')
        self.store = {}
        self.timeout = spec.get("store_timeout", 2)

        self.lock = Lock()

    def getRHT(self):

        try:
            tn = telnetlib.Telnet(self.host, timeout=5)  # reduce waiting time if there is a fault
        except:
            # print('Telnet Connection Error, check IP address', sys.exc_info())
            return 'Telnet Connection Error, check IP address x'
        try:
            tn.read_until(b'>', timeout=1)
        except:
            # print('Vaisala Initialization Error', sys.exc_info())
            return 'Vaisala Initialization Error x'

        tn.write(b'form "RH=" #t 2.2 rh U #t "T=" #t t U #r #n\r')
        try:
            tn.read_until(b'OK\r\n>')
        except:
            # print('Vaisala Format Setup Error', sys.exc_info())
            return 'Vaisala Format Setup Error x'
        tn.write(b'send\r')

        while True:
            try:
                out = tn.read_until(b'\r\n', timeout=1)
            except:
                # print('Vaisala Data Reading Error', sys.exc_info())
                return 'Vaisala Data Reading Error x'
            if (b'C') in out:
                out = out.decode('ascii')
                break
        tn.close()
        return out

    def get_numbers(self):
        data = self.getRHT()
        if data[-1] == 'x':
            return ('NA', 'NA', data)
        else:
            try:
                temp = float(data[15:21])
                humid = float(data[4:9])
                message = 'OK'
            except:
                # print('Bad format, cannot make float.')
                temp = float("NaN")
                humid = float("NaN")
                message = 'Bad format'
            return (temp, humid, message)

    def read_instrument(self, operation_id):
        """
        read instrument 
        """
        try:
            operation = self.operations[operation_id]
        except KeyError:
            print("Invalid operation")
            return float("NaN"), float("NaN")
        # datatype = operation['data_type']
        dtype = operation.get('type', "read_multiple")
        stored = self.store.get(operation_id, (None, time.time()-(self.timeout+1)))
        if time.time() - stored[1] < self.timeout:
            data, data_trans = stored[0]
        else:
            if dtype == 'read_store':
                self.read_instrument(operation.get("store_id"))
                stored = self.store.get(operation_id)
                if time.time() - stored[1] > self.timeout:
                    print('store not updating')
                    return -1, -1
                data, data_trans = stored[0]
                return data, data_trans
            else:
                with self.lock:
                    # print("locK")
                    data = self.get_numbers()

                    data_trans = [self.transform(d, operation) for d in data]

                    o_ops = operation.get("operations")
                    if o_ops is not None:
                        for on in o_ops:
                            o = self.operations.get(on)
                            oi = o.get("store_index")
                            d = data[oi]
                            dt = self.transform(d, o)
                            self.store[on] = ((d, dt), time.time())
                # print('unlocK')
            self.store[operation_id] = ((data, data_trans), time.time())

        return data, data_trans

    def decimals(self, data, operation):
        d_shift = operation.get('decimal_shift', 0)
        d = Decimal(data).scaleb(d_shift)
        f = np.float64(d)
        return f

    def transform(self, data, operation):
        # Bridge transform
        eqb = self.spec.get("bridge_transform", [0, 0])
        # x = data
        eq = operation.get("transform_eq", ['V', 0, 1, 0, 0])
        if self.isfloat(data):  # Check that the data can be transformed
            x = eqb[0] + (1 + eqb[1]) * data
            if eq[0] == 'T':  # Callendar-Van Dusen equation
                if np.isnan(eq[1:4]).any() or np.isinf(eq[1:4]).any() or np.isnan(x) or np.isinf(x):
                    print(f"{x} with transform {eq} is out of range.")
                    transformed = float("NaN")
                else:
                    if x < eq[4]:
                        fulltransformed = np.roots([eq[3], -100 * eq[3], eq[2], eq[1], (1 - (x / eq[4]))])
                    else:
                        fulltransformed = np.roots([eq[2], eq[1], (1 - (x / eq[4]))])
                    transformed = float("inf")  # Create a maximum value
                    for j in fulltransformed:
                        if np.imag(j) == 0:  # Remove imaginary roots
                            if abs(j) < abs(transformed):
                                transformed = np.real(j)  # Find most reasonable real root
                            elif abs(j) == transformed and j > transformed:
                                transformed = np.real(j)  # If the roots are same magnitude, give positive root
                    if math.isinf(transformed):
                        print("Invalid Callendar–Van Dusen equation: No real solutions for")
                        print(f"R = {x}, R0 = {eq[4]}, A = {eq[1]}, B = {eq[2]}, C = {eq[3]}")
                        transformed = float("NaN")
            elif eq[0] == 'V' or eq[0] == 'P':
                transformed = eq[1] + eq[2]*x + eq[3]*x**2 + eq[4]*x**3  # V and P both use cubic equations. P is
                # listed purely for record keeping purposes
            else:
                print(f"Transform form not recognised: {eq[0]}")
                transformed = float("NaN")
        else:
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
    instr = generic_driver_telnet(json.load(open('../instruments/Clients/MSL/Vaisala_HMT331_S0530201.json')))
    print(instr.read_instrument('read_default'))
    print(instr.read_instrument('read_rh'))


if __name__ == '__main__':
    main()
