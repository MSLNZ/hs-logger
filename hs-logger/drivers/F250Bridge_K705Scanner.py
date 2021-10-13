import pyvisa as visa
import time
import numpy as np
import json


class F250Bridge_K705Scanner(object):
    def __init__(self, spec):

        self.spec = spec
        rm = visa.ResourceManager()

        self.bridge = rm.open_resource(spec["port_bridge"])
        self.scanner = rm.open_resource(spec["port_scanner"])
        self.active_channel = 13
        self.bridge.read_termination = '\r\n'

    def read_instrument(self, op_id):
        op = self.spec["operations"][op_id]
        channel = op["channel"]
        prt = op["bridge_prt"]
        self.switch_bridge_prt(prt)

        val = self.read_channel(channel)

        val = val[1:-1]
        if val.startswith("E"):
            val = float("NaN")
        elif val.startswith("A"):
            val = val.replace("A", "")
            val = f = np.float64(val)
        else:
            val = f = np.float64(val)
        val_trans = self.transform(val, op)
        self.open_all_channels()
        return val, val_trans

    def transform(self, data, operation):
        # Bridge transform
        eqb = self.spec.get("bridge_transform", [0, 0])
        x = eqb[0] + (1 + eqb[1]) * data
        # x = data
        eq = operation.get("transform_eq", ['V', 0, 1, 0, 0])
        if eq[0] == 'T':  # Callendar-Van Dusen equation
            if np.isnan(eq[1:4]).any() or np.isinf(eq[1:4]).any() or np.isnan(x) or np.isinf(x):
                transformed = float("NaN")
            else:
                if x < eq[4]:
                    fulltransformed = np.roots([eq[3], -100 * eq[3], eq[2], eq[1], (1 - (x / eq[4]))])
                else:
                    fulltransformed = np.roots([eq[2], eq[1], (1 - (x / eq[4]))])
                transformed = float("inf")  # Create a maximum value
                for j in fulltransformed:
                    if np.imag(j) == 0:
                        if abs(j) < transformed:
                            transformed = np.real(j)
                        elif abs(j) == transformed and j > transformed:
                            transformed = np.real(j)
                if np.isinf(transformed):
                    print("Invalid Callendar–Van Dusen equation: No real solutions for")
                    print("R = {}, R0 = {}, A = {}, B = {}, C = {}".format(x, eq[4], eq[1], eq[2], eq[3]))
                    transformed = float("NaN")
        elif eq[0] == 'V' or eq[0] == 'P':
            transformed = eq[1] + eq[2]*x + eq[3]*x**2 + eq[4]*x**3
        else:
            print("Transform form not recognised: {}".format(eq[0]))
            raise ValueError
        # c = operation.get("transform_coeff", None)
        # transformed = eval(eq)
        return transformed

    def read_channel(self, channel):
        if channel != self.active_channel:
            self.switch_scanner_channel(channel)
        else:
            time.sleep(5)
        time.sleep(1.5)
        i = 0
        while self.bridge.read_stb() != 65:
            i += 1
            if i > 5:
                break
            time.sleep(0.5)
        return self.read()

    def read(self):
        return self.bridge.read()

    def write(self, arg):
        self.bridge.write(arg)

    def switch_scanner_channel(self, channel):
        assert channel in range(11, 21)
        self.open_all_channels()
        # self.scanner.write("N{}X".format(self.active_channel))
        # SCANNER WAIT TIME NEEDED
        time.sleep(1)

        self.scanner.write("C{}X".format(channel))
        self.scanner.write("B{}X".format(channel))
        time.sleep(4)
        self.active_channel = channel

    def open_all_channels(self):
        self.scanner.write("RX")

    def hi_res(self):
        self.bridge.write('R1')

    def unit_ohms(self):
        self.bridge.write('U3')

    def open_channel(self, channel):
        self.write("N{}X".format(channel))

    def read_scanner_channel(self):
        return self.scanner.query("G0")

    def switch_bridge_prt(self, prt):
        # assert prt in ['A','B','C','D','I','J','K','L']
        self.bridge.write("M{}".format(prt))


def main():
    inst = F250Bridge_K705Scanner(json.load(open('../instruments/F250Bridge_K705Scanner.json')))
    print(inst.read_instrument('read_tx_something'))


if __name__ == '__main__':
    main()
