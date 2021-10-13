import pyvisa as visa
import numpy as np
import json
import time


class HP34420A_HP34970A(object):
    def __init__(self, spec):
        rm = visa.ResourceManager()
        self.spec = spec
        self.hp420A = rm.open_resource(spec['port_bridge'])
        self.hp970a = rm.open_resource(spec['port_scanner'])

    def read_instrument(self, op_id):
        op = self.spec["operations"][op_id]
        channel = op["channel"]
        nplc = op["nplc"]
        self.configure_nlpc(nplc)
        val = self.read_channel(channel)
        val = np.float64(val)
        val_trans = self.transform(val, op)
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
        self.switch_scanner_channel(channel)
        return self.read()

    def configure_nlpc(self, nplc):
        assert nplc in [0.02, 0.2, 1, 2, 10, 20, 100, 200, 'MIN', 'MAX']
        self.hp420A.write("VOLT:NPLC {}".format(nplc))

    def read(self):
        return self.hp420A.query("READ?")

    def write(self, arg):
        self.hp420A.write(arg)

    def switch_scanner_channel(self, channel):
        self.hp970a.write("MEAS:VOLT:DC? (@{})".format(channel))
        val = self.hp970a.read()


def main():
    inst = HP34420A_HP34970A(json.load(open('../instruments/HP34420A_HP34970A.json')))
    print(inst.read_instrument('read_px120'))


if __name__ == '__main__':
   main()
