import sys
import pumpy
import logging
import time

from progress.bar import ChargingBar

def infuseProg(flowRate, targetVol):
  totalDur = ((1/flowRate)*targetVol) * 60
  delayDur = totalDur/20
  bar = ChargingBar('Infusing', max=20)
  for i in range(20):
      time.sleep(delayDur)
      bar.next()
  bar.finish()


logging.basicConfig(level=logging.INFO)

chain = pumpy.Chain('../../../../../dev/ttyUSB0')
PHDcoll = pumpy.PHD2000(chain,address=1, name="PHDcollagen") # PHD2000
PHDha = pumpy.PHD2000(chain,address=12, name="PHDhaNP") # special pump

# Set diameters
PHDcoll.setdiameter(25)
PHDha.setdiameter(25)
# Set Flow Rates
PHDcoll.setflowrate(600)
PHDha.setflowrate(600)
# Set each target volume for each infuse.
PHDcoll.settargetvolume(2000)
PHDha.settargetvolume(2000)


for i in range(0,20):
  PHDcoll.infuse()
  logging.info('Collagen: infusing, cycle ' + str(i))
  infuseProg(600, 2000)
  PHDcoll.stop()
  logging.info('Collagen: stopped infusing, cycle ' + str(i))
  PHDha.infuse()
  infuseProg(600, 2000)
  logging.info('HAnp: infusing, cycle ' + str(i))
  PHDha.stop()
  logging.info('HAnp: stopped infusing, cycle ' + str(i))

sys.exit()
