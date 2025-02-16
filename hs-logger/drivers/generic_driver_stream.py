import pyvisa as visa
import json
import time
from decimal import Decimal
from threading import Lock
import numpy as np
import math
import re


class generic_driver_stream(object):

    def __init__(self, spec):
        """This driver expects to receive information on:
        port, baud rate, read/write terms
        It can also accept doOpen = False, which will skip the open instrument command"""
        self.spec = spec
        self.operations = spec.get('operations', {})
        port = spec["port"]  # Port is required and can't be generalised.
        baud = spec.get("baudrate", 9600)
        r_term = spec.get("read_termination", '\r\n')
        doOpen = spec.get("doOpen", True)
        rm = visa.ResourceManager()
        self.store = {}
        self.timeout = spec.get("store_timeout", 2)
        self.instrument = rm.open_resource(port,
                                           baud_rate=baud,
                                           read_termination=r_term)
        if doOpen:
            self.instrument.open()
        self.instrument.timeout = 2000
        self.lock = Lock()

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
        dtype = operation.get('type', "read_single")
        echo = self.spec.get('echo', False)
        stored = self.store.get(operation_id, (None, time.time()-(self.timeout+1)))
        if time.time() - stored[1] < self.timeout:
            data, data_trans = stored[0]
        else:
            with self.lock:
                # print("locK")
                data = float("NaN")
                try:
                    while True:
                        data = self.instrument.read()
                        print(data)
                except visa.errors.VisaIOError as e:
                    # print(e)
                    pass
                try:
                    regx = re.compile(r'-?\d{1,2}\.\d')
                    d = regx.search(data)
                    data = d.group()
                    data = float(data)
                except (ValueError, TypeError, AttributeError):
                    data = float("NaN")
                data_trans = self.transform(data, operation)
                # print('unlocK')
            self.store[operation_id] = ((data, data_trans), time.time())

        return data, data_trans

    def write_instrument(self, operation_id, values):
        with self.lock:
            """
            write instrument 
            """
            try:
                op = self.operations[operation_id]
            except KeyError:
                print("Invalid operation")
                return float("NaN"), float("NaN")
            command = op.get("command", "")
            command = command.format(*values)
            # response = self.instrument.query(command)
            response = ""
            self.instrument.write(command)
            try:
                while True:
                    if response == "":
                        response = self.instrument.read()
                    else:
                        response = response + ", " + self.instrument.read()
            except visa.errors.VisaIOError:
                pass
            if response != "":
                print(response)
            else:
                print("No response")
            return response

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
    instr = generic_driver_stream(json.load(open('../instruments/Edgetech_Dewmaster.json')))


if __name__ == '__main__':
    main()
