import json
import math
import struct
import serial
import numpy as np
from threading import Lock
import time


class SFC5XXX_driver(object):

    def __init__(self, spec):
        self.spec = spec
        self.operations = spec['operations']
        port = spec["port"]
        baud = spec["baudrate"]
        par = spec["parity"]
        stop_b = spec["stopbits"]
        time_out = spec["timeout"]
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

        self.adr = spec["address"]
        self.abyte = ["b", "u8t", "i8t"]
        self.bbyte = ["u16t", "i16t"]
        self.cbyte = ["f", "u32t", "i32t"]
        self.dbyte = ["u64t", "i64t"]

        self.lock = Lock()

    def read_instrument(self, op_id):
        operation = self.operations[op_id]
        with self.lock:
            # print("locK")
            cid = operation.get('command_id', 0)
            data = operation['din']
            mositype = operation['mosi_dtype']
            misotype = operation['miso_dtype']
            if data is list:
                feed = data
            else:
                feed = [data]
            cmd = self.mosi(self.adr, cid, feed, mositype)
            self.instrument.write(cmd)
            frame = self.instrument.read_until(bytes(126))
            print(frame)
            try:
                data = self.miso(frame, misotype)
            except ValueError:
                data = float("NaN")
            data = float(data[0])

            data_trans = self.transform(data, operation)
        print(data, data_trans)
        return data, data_trans

    def write_instrument(self, op_id, data):
        with self.lock:
            operation = self.operations[op_id]
            cid = operation.get('command_id', 0)
            mositype = operation['mosi_dtype']
            misotype = operation['miso_dtype']
            if data is list:
                feed = data
            else:
                feed = [data]
            cmd = self.mosi(self.adr, cid, feed, mositype)
            self.instrument.write(cmd)

            response = self.miso(str(self.instrument.read_until(self.r_term)), misotype)

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
                    print("{} with transform {} is out of range.".format(x,eq))
                    transformed = float("NaN")
                else:
                    if x < eq[4]:
                        fulltransformed = np.roots([eq[3], -100 * eq[3], eq[2], eq[1], (1 - (x / eq[4]))])
                    else:
                        fulltransformed = np.roots([eq[2], eq[1], (1 - (x / eq[4]))])
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
                transformed = eq[1] + eq[2]*x + eq[3]*x**2 + eq[4]*x**3  # V and P both use cubic equations. P is
                # listed purely for record keeping purposes
            else:
                print("Transform form not recognised: {}".format(eq[0]))
                transformed = float("NaN")
        else:
            transformed = float("NaN")  # The data can't be transformed
        # c = operation.get("transform_coeff", None)
        # transformed = eval(eq)
        return transformed

    def isfloat(self, data):
        try:
            float(data)  # Checks if the string can be made into a float.
            return True
        except ValueError:
            return False

    def miso(self, frame, dtype):
        """
        convert frame to data
        """
        framelist = list(frame)
        # remove start and stop bits
        framelist = framelist[1:-1]
        # undo byte stuffing
        temp = []
        skip = False
        for i in range(len(framelist)):
            if framelist[i] == 125:
                skip = True
                if framelist[i + 1] == 94:
                    temp.append(126)
                elif framelist[i + 1] == 93:
                    temp.append(125)
                elif framelist[i + 1] == 49:
                    temp.append(17)
                elif framelist[i + 1] == 51:
                    temp.append(19)
                else:
                    print("byte stuffing wrong: {} not an acceptable next character".format(framelist[i + 1]))
                    raise ValueError
            else:
                if skip:
                    skip = False
                else:
                    temp.append(framelist[i])
        framelist = temp
        # check the checksum
        chk = framelist[-1]
        framelist = framelist[:-1]
        framesum = sum(framelist)
        LSB = framesum % 256
        checksum = 255 - LSB
        if chk != checksum:
            print("checksum wrong: {} != {}".format(chk, checksum))
            raise ValueError
        # extract variables
        adr = framelist[0]
        framelist = framelist[1:]
        cmd = framelist[0]
        framelist = framelist[1:]
        state = framelist[0]
        framelist = framelist[1:]
        l = framelist[0]
        framelist = framelist[1:]
        # check the length
        length = len(framelist)
        if l != length:
            print("length wrong: {} != {}".format(l, length))
            raise ValueError
        # check state if required
        if state != 0:
            if 0 < state < 32:
                print("state wrong: common error {}".format(state))
                raise ValueError
            else:
                print("state wrong: specific error {}".format(state))
                raise ValueError
        # convert data from bytes to appropriate data type
        temp = []
        for i in range(len(dtype)):
            # turn data into a list of datums.
            if dtype[i] in self.abyte:
                byte = []
                byte.append(framelist[0])
                temp.append(byte)
                if len(framelist) > 1:
                    framelist = framelist[1:]
                else:
                    break
            elif dtype[i] in self.bbyte:
                temp.append(framelist[0:2])
                if len(framelist) > 2:
                    framelist = framelist[2:]
                else:
                    break
            elif dtype[i] in self.cbyte:
                temp.append(framelist[0:4])
                if len(framelist) > 4:
                    framelist = framelist[4:]
                else:
                    break
            elif dtype[i] in self.dbyte:
                temp.append(framelist[0:8])
                if len(framelist) > 8:
                    framelist = framelist[8:]
                else:
                    break
            elif dtype[i] == "s":
                # Strings have variable length
                string = []
                for i in range(len(framelist)):
                    if framelist[i] != 0:
                        string.append(framelist[i])  # Record the byte
                    else:
                        framelist = framelist[i+1:]
                        break
                temp.append(string)
            else:
                print("dtype wrong: {} is not a valid data type".format(dtype))
                raise ValueError
        framelist = temp
        data = []
        for i in range(len(framelist)):
            d = framelist[i]
            b = bytes(d)  # convert d to a single list of bits
            n = float("NaN")
            if dtype[i].startswith("b"):  # Data is a boolean
                n = struct.unpack('>?', b)[0]
            elif dtype[i].startswith("f"):  # Data is a float
                n = struct.unpack('>f', b)[0]
            elif dtype[i].startswith("s"):  # Data is a string
                n = b.decode('unicode_escape')
            elif dtype[i].startswith("u8t"):  # Data is an unsigned integer of length 1
                n = struct.unpack('>B', b)[0]
            elif dtype[i].startswith("u16t"):  # Data is an unsigned integer of length 2
                n = struct.unpack('>H', b)[0]
            elif dtype[i].startswith("u32t"):  # Data is an unsigned integer of length 4
                n = struct.unpack('>I', b)[0]
            elif dtype[i].startswith("u64t"):  # Data is an unsigned integer of length 8
                n = struct.unpack('>Q', b)[0]
            elif dtype[i].startswith("i8t"):  # Data is a signed integer of length 1
                n = struct.unpack('>b', b)[0]
            elif dtype[i].startswith("i16t"):  # Data is a signed integer of length 2
                n = struct.unpack('>h', b)[0]
            elif dtype[i].startswith("i32t"):  # Data is a signed integer of length 4
                n = struct.unpack('>i', b)[0]
            elif dtype[i].startswith("i64t"):  # Data is a signed integer of length 8
                n = struct.unpack('>q', b)[0]
            else:
                print("dtype wrong: {} is not a valid data type".format(dtype))
                raise ValueError
            data.append(n)
        return data

    def mosi(self, adr, cmd, data, dtype):
        """
        convert data to frame
        """
        framelist = []
        # convert data from given data type to bytes
        for i in range(len(data)):
            if dtype[i].startswith("b"):  # Data is a boolean
                framelist.append(list(struct.pack('>?', data[i])))
            elif dtype[i].startswith("f"):  # Data is a float
                framelist.append(list(struct.pack('>f', data[i])))
            elif dtype[i].startswith("s"):  # Data is a string
                framelist.append(list(data[i].encode('unicode_escape')))
                framelist[-1].append(0)
            elif dtype[i].startswith("u8t"):  # Data is an unsigned integer of length 1
                framelist.append(list(struct.pack('>B', data[i])))
            elif dtype[i].startswith("u16t"):  # Data is an unsigned integer of length 2
                framelist.append(list(struct.pack('>H', data[i])))
            elif dtype[i].startswith("u32t"):  # Data is an unsigned integer of length 4
                framelist.append(list(struct.pack('>I', data[i])))
            elif dtype[i].startswith("u64t"):  # Data is an unsigned integer of length 8
                framelist.append(list(struct.pack('>Q', data[i])))
            elif dtype[i].startswith("i8t"):  # Data is a signed integer of length 1
                framelist.append(list(struct.pack('>b', data[i])))
            elif dtype[i].startswith("i16t"):  # Data is a signed integer of length 2
                framelist.append(list(struct.pack('>h', data[i])))
            elif dtype[i].startswith("i32t"):  # Data is a signed integer of length 4
                framelist.append(list(struct.pack('>i', data[i])))
            elif dtype[i].startswith("i64t"):  # Data is a signed integer of length 8
                framelist.append(list(struct.pack('>q', data[i])))
            else:
                print("dtype wrong: {} is not a valid data type".format(dtype))
                raise ValueError
        temp = []
        for f in framelist:
            for b in f:
                temp.append(b)
        framelist = temp
        # produce the length
        length = len(framelist)
        # add variables
        framelist.insert(0, length)
        framelist.insert(0, cmd)
        framelist.insert(0, adr)
        # generate the checksum
        framesum = sum(framelist)
        LSB = framesum % 256
        checksum = 255 - LSB
        framelist.append(checksum)
        # perform byte stuffing
        temp = []
        for byte in framelist:
            if byte == 126:
                temp.append(125)
                temp.append(94)
            elif byte == 125:
                temp.append(125)
                temp.append(93)
            elif byte == 17:
                temp.append(125)
                temp.append(49)
            elif byte == 19:
                temp.append(125)
                temp.append(51)
            else:
                temp.append(byte)
        framelist = temp
        # add start and stop bits
        framelist.insert(0, 126)
        framelist.append(126)
        frame = bytes(framelist)
        return frame


def main():
    instr = SFC5XXX_driver(json.load(open('../instruments/SFC5XXX.json')))
    adr = 1
    cmd = 2
    dtypelist = [["u8t", "b", "f", "s"], ["u8t", "u8t", "u8t"], ["u16t", "u16t", "u16t"], ["u32t", "u32t", "u32t"],
                 ["u64t", "u64t", "u64t"], ["i8t", "i8t", "i8t"], ["i16t", "i16t", "i16t"], ["i32t", "i32t", "i32t"],
                 ["i64t", "i64t", "i64t"], ["b", "b"], ["f", "f", "f", "f"], ["s", "s", "s"], []]
    datalist = [[12, True, 0.15625, "TEST"], [0, 127, 255], [0, 32768, 65535], [0, 2147483648, 4294967295],
                [0, 9223372036854775808, 18446744073709551615], [-128, 0, 127], [-32768, 0, 32767],
                [-2147483648, 0, 2147483647], [-9223372036854775808, 0, 9223372036854775807], [True, False],
                [0, 0.15625, float("NaN"), float("Inf")], ["This", "Should", "Work"], []]
    for i in range(len(dtypelist)):
        dtype = dtypelist[i]
        data = datalist[i]
        frame = instr.mosi(adr, cmd, data, dtype)
        frame = list(frame)
        frame.insert(3, 0)
        frame = bytes(frame)
        redata = instr.miso(frame, dtype)
        if data == redata:
            print("Pass {}".format(dtype))
        else:
            print("Fail {}: {} is not equal to {}".format(dtype, data, redata))  # Float will fail because NaN != NaN


if __name__ == '__main__':
    main()
