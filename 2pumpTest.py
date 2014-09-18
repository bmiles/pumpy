import pumpy
import sys

chain = pumpy.Chain('../../../../../dev/ttyUSB0')
phd = pumpy.PHD2000(chain,address=1, name="Pump1") # PHD2000
phd2 = pumpy.PHD2000(chain,address=12, name="Pump2") # special pump

phd2.setdiameter(25)
phd.setdiameter(25)

phd.setflowrate(600)
phd2.setflowrate(600)

phd.settargetvolume(200)
phd2.settargetvolume(200)

phd.infuse()
phd.stop()
phd2.infuse()
phd2.stop()

sys.exit()
