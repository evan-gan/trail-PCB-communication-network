from lib.sx1262 import SX1262
import json


class Radio:
    def __init__(self):
        self.sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12,
                         cs=3, irq=20, rst=15, gpio=2)

        self.sx.begin(freq=902.0, bw=500.0, sf=12, cr=8, syncWord=0x12,
                      power=4,  # Our antenna's max power is 5 dBm
                      currentLimit=60.0, preambleLength=8,
                      implicit=False, implicitLen=0xFF,
                      crcOn=True, txIq=False, rxIq=False,
                      tcxoVoltage=0, useRegulatorLDO=False, blocking=True)

        self.sx.setBlockingCallback(False, self.onReceive)

        self.received_messages = []

    def onReceive(self, events):
        if events & SX1262.RX_DONE:
            message, error = self.sx.recv()

            error = SX1262.STATUS[error]

            print('Received {}, {}'.format(message, error))

            if error == "ERR_NONE":
                message_dict = json.loads(message.decode("utf-8"))
                self.received_messages.append(message_dict)
        elif events & SX1262.TX_DONE:
            print('done transmitting')
        pass

    def sendMSG(self, message):
        self.sx.send(json.dumps(message).encode("utf-8"))
