import visa

# NOT COMLEATED
#READ TERMINATION IMPORTATNT TO SET to '\n'

class F250Bridge_K705Scanner(object):
    def __init__(self,bridge_address,scanner_address):
        rm = visa.ResourceManager()

        self.bridge = rm.open_resource(bridge_address)
        self.scanner = rm.open_resource(scanner_address)
        self.active_channel = 13
        self.bridge.read_termination = '\n'

    def read_channel(self,channel):
        self.switch_scanner_channel(channel)
        # TODO Check SRQ here
        # while self.bridge
        return self.read()

    def read(self):
        return self.bridge.read()

    def write(self,arg):
        self.bridge.write(arg)

    def switch_scanner_channel(self,channel):
        assert channel in range(11, 20)
        self.open_all_channels()
        #self.scanner.write("N{}X".format(self.active_channel))
        # SCANNER WAIT TIME NEEDED


        self.scanner.write("B{}X".format(channel))
        self.scanner.write("C{}X".format(channel))
        self.active_channel = channel



    def open_all_channels(self):
        self.scanner.write("RX")

    def close_channel(self,channel):
        self.write("N{}X".format((channel)))

    def read_scanner_channel(self):
        return self.scanner.query("G0")

    def switch_bridge_prt(self,prt):
        # assert prt in ['A','B','C','D','I','J','K','L']
        self.scanner.write("M{}".format(prt))

def main():
    inst = F250Bridge_K705Scanner("GPIB0::3::INSTR","GPIB0::17::INSTR")
    inst.switch_bridge_prt('A')
    print(inst.read_channel(12))
    print(inst.read_channel(13))
if __name__ == '__main__':
    main()



