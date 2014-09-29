import sys
import pumpy
import logging
import time
import os
# Push notification stuff

import httplib, urllib

pushover_user_key = os.environ['PUSHOVER_USER_KEY']
pushover_app_key = os.environ['PUSHOVER_PUMPY_APP_TOKEN']


def push(message):
  conn = httplib.HTTPSConnection("api.pushover.net:443")
  conn.request("POST", "/1/messages.json",
    urllib.urlencode({
      "token": pushover_app_key,
      "user": pushover_user_key,
      "message": message,
    }), { "Content-type": "application/x-www-form-urlencoded" })
  conn.getresponse()

# from progress.bar import ChargingBar
#
# def infuseProg(flowRate, targetVol):
#   totalDur = ((1/flowRate)*targetVol) * 60
#   delayDur = totalDur/20
#   bar = ChargingBar('Infusing', max=20)
#   for i in range(20):
#       time.sleep(delayDur)
#       bar.next()
#   bar.finish()


logging.basicConfig(level=logging.INFO)

chain = pumpy.Chain('../../../../../dev/ttyUSB0')
PHDcoll = pumpy.PHD2000(chain,address=1, name="PHDcollagen") # PHD2000
PHDha = pumpy.PHD2000(chain,address=12, name="PHDhaNP") # special pump

tVol = 2000 # 2mL
tTime = 60 # 60 minutes
flowRate = tVol/tTime
cycles = 21 #21 does 20 cycles

# Set diameters BD plastpak 50/60mL
PHDcoll.setdiameter(26.7)
PHDha.setdiameter(26.7)
# Set Flow Rates
PHDcoll.setflowrate(flowRate)
PHDha.setflowrate(flowRate)
# Set each target volume for each infuse.
PHDcoll.settargetvolume(tVol)
PHDha.settargetvolume(tVol)


for i in range(0,cycles):
  push("Starting Collagen cycle: " + str(i))
  PHDcoll.infuse()
  logging.info('Collagen: infusing, cycle ' + str(i))
  PHDcoll.waituntiltarget()
  PHDcoll.stop()
  logging.info('Collagen: stopped infusing, cycle ' + str(i))
  push("Starting Hydroxyapatite cycle: " + str(i))
  PHDha.infuse()
  logging.info('HAnp: infusing, cycle ' + str(i))
  PHDha.waituntiltarget()
  PHDha.stop()
  logging.info('HAnp: stopped infusing, cycle ' + str(i))

push("Job Complete :)")
sys.exit()
