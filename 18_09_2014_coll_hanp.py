import sys
import pumpy

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
PHDcoll.settargetvolume(200)
PHDha.settargetvolume(200)


for i in range(0,20)
  PHDcoll.infuse()
  print('Collagen: infusing cycle ' + i)
  PHDcoll.stop()
  print('Collagen: stopped infusing cycle ' + i)
  PHDha.infuse()
  print('HAnp: infusing cycle ' + i)
  PHDha.stop()
  print('HAnp: stopped infusing cycle ' + i)

sys.exit()
