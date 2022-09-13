import json
import time
import thorlabs_apt as apt
# install apt user from the thorlabs website.  Select correct one


class Thorlabs_stage_driver(object):

    def __init__(self, spec):
        self.spec = spec
        # print(spec)
        devices = apt.list_available_devices()
        # print(devices)
        nr_devices = len(devices)
        if nr_devices == 0:
            print("Not recognised a device.  Unplug USB and try again.  Use APT user to check if device shows up.")
            raise ValueError
        else:
            dev_snr = devices[0][1]
        self.device = apt.Motor(dev_snr)
        self.operations = spec.get('operations', {})

    def read_instrument(self, op_id):
        if op_id == "read_pos":  # operation = self.operations[operation_id]
            val = self.device.position
        else:
            val = float("NaN")
        return val, val

    def write_instrument(self, op_id, message):
        message = float(message[0])
        if op_id == "move_to":
            val = self.device.move_to(message)
            in_motion = True

        elif op_id == "move_by":
            val = self.device.move_by(message)
            in_motion = True

        else:
            val = float("NaN")
            in_motion = False

        while in_motion:
            time.sleep(1)
            in_motion = self.device.is_in_motion
        return val


def main():
    # testing
    instr = Thorlabs_stage_driver(json.load(open('../instruments/Thorlabs_stage_45843029.json')))
    # instr.write_instrument('write_Valve_index', 1)
    # print(instr.read_instrument('read_Tm'))
    position = instr.read_instrument('read_pos')
    while position < 20:
        instr.write_instrument('move_by', [1])
        position = instr.read_instrument('read_pos')
        print(position)
        time.sleep(1)

    # instr.write_instrument('move_to', [1])
    # print(instr.read_instrument('position'))


if __name__ == '__main__':
    main()