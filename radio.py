from lib.sx1262 import SX1262
# from main import name # needs to be implemented
import time

name = "D1"

def cb(events):
    if events & SX1262.RX_DONE:
        msg, err = sx.recv()
        error = SX1262.STATUS[err]
        print('Received {}, {}'.format(msg, error))
        if error == "ERR_NONE":
            if str(msg).split("|")[0] == name:
                recivedMSG(str(msg).split("|")[1]) # needs to be implemented
    elif events & SX1262.TX_DONE:
        print('done transmitting')
    pass

sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)
sx.begin(freq=902.0, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=0, useRegulatorLDO=False, blocking=True)
sx.setBlockingCallback(False, cb)

def sendMSG(msg, recp):
    sx.send(bytes(recp + "|" + msg))

def recivedMSG(MSG):
    print(MSG)