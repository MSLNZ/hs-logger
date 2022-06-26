import math
import json
import sys
import os


class PID_driver(object):

    def __init__(self, spec):
        self.spec = spec

        # Create variables for PID control.
        self.hs_address = os.getcwd()
        self.r = float("NaN")  # Setpoint value
        self.y = 0  # Measured value
        self.e = 0  # Error value
        self.u = 0  # Control value
        self.Ppt = spec.get("Proportional", 0.5)
        self.Itg = spec.get("Integral", 0)
        self.Dvt = spec.get("Derivative", 0)
        self.history = []
        self.max = spec.get("max")
        self.min = spec.get("min")

        if spec.get("sign", True):
            self.sign = 1
        else:
            self.sign = -1

        # Perform loading functions for Read and Write
        self.read, self.write = self.load_operations([spec.get("measure"), spec.get("control")])

        # Initialize self.u
        try:
            instrument = json.load(open(self.hs_address + "\\instruments\\" + spec.get("control")[0]))
            init = instrument["operations"][self.write[1]].get("check_set", "")
            inst_w = self.write[0]
            if init in instrument["operations"]:
                self.u = inst_w.read_instrument(init)[1]  # Write the control variable
        except (OSError, ValueError):
            sys.stderr.write("Error loading instrument: {}".format(spec.get("control")[0]))
            sys.exit(1)

    def read_instrument(self, op_id):
        # In this section, read the instrument, update the control settings, and write to the control.
        if op_id == "setpoint_check":
            return self.r, self.r
        else:
            inst_r = self.read[0]
            result = inst_r.read_instrument(self.read[1])
            self.y = result[1]  # Read the measured value

            if math.isnan(self.r):
                return float("NaN"), self.y
            self.e = self.sign*(self.r - self.y)
            self.history.append(self.e)
            p = self.e*self.Ppt  # Calculate proportional component
            i = sum(self.history)*self.Itg  # Calculate integral component
            if len(self.history) < 2:
                d = 0  # Not enough points for slope calculation, use 0
            else:
                d = (self.history[-1] - self.history[-2])*self.Dvt  # Calculate derivative component
            self.u = self.u + p + i + d

            output = self.u  # Todo This might need to change. Otherwise, remove output.
            if output > self.max:
                output = self.max
            if output < self.min:
                output = self.min
            inst_w = self.write[0]
            inst_w.write_instrument(self.write[1], [output])  # Write the control variable
            # print("Y:{}, R:{}, E:{}, P:{}, I:{}, D:{}, U:{}".format(self.y, self.r, self.e, p, i, d, self.u))
            return output, self.y

    def write_instrument(self, op_id, message):
        # All this does is change the set value and clear the history.
        command = "{}".format(*message)
        self.r = float(command)
        if self.r > self.max:
            self.r = self.max
            print("{} is the maximum control value".format(self.max))
        if self.r < self.min:
            self.r = self.min
            print("{} is the minimum control value".format(self.min))
        self.history = []  # This prevents integral buildup and derivative spikes

    def load_operations(self, op_spec):
        # op_spec is a 2x2 array of the specific instrument and operation that should be read or written.
        operations = []
        instruments = {}
        for i in range(len(op_spec)):
            inst_id = op_spec[i][0]
            operation = op_spec[i][1]
            if inst_id in instruments:
                instrument = instruments[inst_id]
            else:
                try:
                    instrument = json.load(open(self.hs_address + "\\instruments\\" + op_spec[i][0]))
                except (OSError, ValueError):
                    sys.stderr.write("Error loading instrument: {}".format(op_spec[i]))
                    sys.exit(1)
                driver_name = instrument["driver"]

                # Check if op is in inst
                if operation in instrument["operations"]:
                    if "transducer" in instrument["operations"][operation]:
                        td = json.load(open(instrument["operations"][operation]["transducer"]))
                        instrument["operations"][operation].update(td)
                        names = []
                        if instrument["operations"][operation]["t_name"] != "":
                            names.append(instrument["operations"][operation]["t_name"])
                        if instrument["operations"][operation]["t_id"] != "":
                            names.append(instrument["operations"][operation]["t_id"])
                        names.append(instrument["operations"][operation]["name"])
                        c_name = " "
                        c_name = c_name.join(names)
                        instrument["operations"][operation]["name"] = c_name
                else:
                    sys.stderr.write("Operation not in instrument: {}".format(op_spec[i]))
                    sys.exit(1)

                driver = getattr(__import__("drivers." + driver_name), driver_name)
                klass = getattr(driver, driver_name)
                inst_driver = klass(instrument)
                instruments[inst_id] = [inst_driver, instrument]
            operations.append([instruments[inst_id][0], operation])

        return operations


def main():
    pass
