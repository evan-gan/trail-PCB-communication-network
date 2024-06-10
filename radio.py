from lib.sx1262 import SX1262


class Radio:
    def __init__(self, receivedMSG):
        self.sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12,
                         cs=3, irq=20, rst=15, gpio=2)
        self.sx.begin(freq=902.0, bw=500.0, sf=12, cr=8, syncWord=0x12,
                      power=5,  # Our antenna's max power is 5 dBm
                      currentLimit=60.0, preambleLength=8,
                      implicit=False, implicitLen=0xFF,
                      crcOn=True, txIq=False, rxIq=False,
                      tcxoVoltage=0, useRegulatorLDO=False, blocking=True)
        self.receivedMSG = receivedMSG
        self.sx.setBlockingCallback(False, self.cb)

    def cb(self, events):
        if events & SX1262.RX_DONE:
            msg, err = self.sx.recv()
            error = SX1262.STATUS[err]
            print('Received {}, {}'.format(msg, error))
            if error == "ERR_NONE":
                # if msg[1] == myname: # this line will only work once changing name is implemented
                self.receivedMSG(str(msg))

        elif events & SX1262.TX_DONE:
            print('done transmitting')
        pass

    def sendMSG(self, msg, frm, to):  # frm = from
        # sx.send(bytes(f"{frm}|{to}|{msg}", 'utf-8'))
        self.sx.send(bytes(f"{frm}: {msg}", 'utf-8'))
