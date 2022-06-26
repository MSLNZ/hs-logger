import random


class dummy_driver(object):

    def __init__(self, spec):
        self.spec = spec
        self.setpoint = 1
        pass

    def read_instrument(self, op_id):
        """
        read instrument
        """
        if op_id == "setpoint_test":
            return self.setpoint, self.setpoint
        else:
            v = random.random()
            w = 2 * self.setpoint - 1 + ((v - 0.5) * self.setpoint / 10)
            return v, w

    def write_instrument(self, op_id, message):
        """
        write instrument
        """
        self.setpoint = float("{}".format(*message))
        return "not here"


def main():
    pass


if __name__ == '__main__':
    main()
