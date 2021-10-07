import random


class dummy_driver(object):

    def __init__(self, spec):
        self.spec = spec
        pass

    def read_instrument(self, op_id):
        """
        read instrument s
        """
        if op_id == "setpoint_test":
            return 0
        else:
            v = random.random()
            w = 1+v
            return v, w

    def write_instrument(self, op_id, message):
        """
        write instrument
        """
        return "not here"


def main():
    pass


if __name__ == '__main__':
    main()
