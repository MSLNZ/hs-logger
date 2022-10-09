import json
import numpy as np
import math

from threading import Lock
import serial
import time
import re
import binascii
# from calcCRC import calcCRC

class Driver_SmartTrak_pyserial(object):

    def __init__(self, spec):
        """This driver expects to receive information on:
        port, baud rate, parity, stop bits, timeout, read/write terms"""
        self.spec = spec
        self.operations = spec.get('operations', {})
        port = spec["port"]  # Port is required and can't be generalised.
        baud = spec.get("baudrate", 9600)
        par = spec.get("parity", "NONE")
        stop_b = spec.get("stopbits", 1)
        time_out = spec.get("timeout", 0)
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

        if stop_b == "2":
            self.instrument.stopbits = serial.STOPBITS_TWO
        elif stop_b == "1.5":
            self.instrument.stopbits = serial.STOPBITS_ONE_POINT_FIVE
        else:
            self.instrument.stopbits = serial.STOPBITS_ONE

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

        stored = self.store.get(operation_id, (None, time.time() - (self.timeout + 1)))  # what is this?

        if time.time() - stored[1] < self.timeout:
            data, data_trans = stored[0]
        else:
            if dtype == 'read_single':
                with self.lock:
                    # print("locK")
                    cmd = operation.get('command', "")
                    crc = calcCRC(cmd)
                    cmd_e = cmd.encode("ascii") + crc + self.w_term.encode("ascii")
                    self.instrument.write(cmd_e)
                    data = self.instrument.read_until(self.r_term)
                    floats_data = re.findall(r"[-+]?\d*\.\d+|\d+", str(data))
                    data = float(floats_data[0])

                    data_trans = self.transform(data, operation)
                # print('unlocK')
            else:
                with self.lock:
                    # print("lock")
                    print(operation.get('command', ""))
                    cmd_e = (operation.get('command', "")).encode("ascii") + self.w_term.encode("ascii")
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
            try:
                op = self.operations[operation_id]
            except KeyError:
                print("Invalid operation")
                return float("NaN"), float("NaN")
            command = op.get("command", "")
            command = command.format(*values)

            cmd_e = command.encode("ascii") + calcCRC(command) + self.w_term.encode("ascii")

            # response = self.instrument.query(command)
            # cmd_e = command.encode("ascii") + self.w_term.encode("ascii")
            self.instrument.write(cmd_e)

            response = str(self.instrument.read_until(self.r_term))

            if response != "":
                pass  # print(response)
            else:
                print("No response")
            return response

    def transform(self, data, operation):
        x = data
        eq = operation.get("transform_eq", ['V', 0, 1, 0, 0])
        if self.isfloat(data):  # Check that the data can be transformed
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
                transformed = eq[1] + eq[2] * x + eq[3] * x ** 2 + eq[4] * x ** 3
                # V and P both use cubic equations. P is listed purely for record keeping purposes
            else:
                print(f"Transform form not recognised: {eq[0]}")
                transformed = float("NaN")
        else:
            print(f"{x} can't be transformed.")
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


def calcCRC(cmnd):
    # cmnd is a byte array containing the command ASCII string; example: cmnd="Sinv2.000"
    # an unsigned 32 bit integer is returned to the calling program
    # only the lower 16 bits contain the crc

    crc = 0xffff  # initialize crc to hex value 0xffff

    for character in cmnd:  # this for loop starts with ASCCII 'S' and loops through to the last ASCII '0'
        hex_char = (int(ord(character)))
        # hex_char = character
        crc = crc ^ (hex_char * 0x0100)  # the ASCII value is times by 0x0100 first then XORED to the current crc value
        # for(j=0; j<8; j++) # the crc is hashed 8 times with this for loop
        j = 0
        for j in range(0, 8):
            # if the 15th bit is set (tested by ANDING with hex 0x8000 and testing for 0x8000 result)
            # then crc is shifted left one bit (same as times 2) XORED with hex 0x1021 and ANDED to
            # hex 0xffff to limit the crc to lower 16 bits. If the 15th bit is not set then the crc
            # is shifted left one bit and ANDED with hex 0xffff to limit the crc to lower 16 bits.
            if (crc & 0x8000) == 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xffff
            else:
                crc = (crc << 1) & 0xffff
            # end of j loop
        # end of i loop
    # There are some crc values that are not allowed, 0x00 and 0x0d

    # These are byte values so the high byte and the low byte of the crc must be checked and incremented if
    # the bytes are either 0x00 0r 0x0d
    if (crc & 0xff00) == 0x0d00:
        crc += 0x0100
    if (crc & 0x00ff) == 0x000d:
        crc += 0x0001
    if (crc & 0xff00) == 0x0000:
        crc += 0x0100
    if (crc & 0x00ff) == 0x0000:
        crc += 0x0001

    crc_hex_string = str(hex(crc))
    if len(crc_hex_string) < 6:
        crc_hex_string_final = crc_hex_string[:2] + '0' + crc_hex_string[2:]
    else:
        crc_hex_string_final = crc_hex_string
    first_byte = crc_hex_string_final[2:4]
    second_byte = crc_hex_string_final[4:6]
    # final = binascii.unhexlify('66666666')
    final = binascii.unhexlify(first_byte + second_byte)
    # print('final= ')
    # print (final)

    return final

    # If the string Sinv2.000 is sent through this routine the crc = 0x8f55
    # The complete command "Sinv2.000" will look like this in hex:
    # 0x53 0x69 0x6E 0x76 0x32 0x2e 0x30 0x30 0x30 0x8f 0x55 0x0d


# testing
def main():
    instr = Driver_SmartTrak_pyserial(json.load(open('../instruments/SmartTrak100.json')))
    # instr.write_instrument('write_Valve_index', 1)
    # print(instr.read_instrument('read_Tm'))
    instr.write_instrument('write_setpoint', [0.3])
    print(instr.read_instrument('read_flow'))

    instr.write_instrument('write_Valve_index', [1])


if __name__ == '__main__':
    main()
