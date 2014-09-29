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
      "token": pushover_user_key,
      "user": pushover_app_key,
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
tTime = 30 # 60 minutes
flowRate = tVol/tTime
cycles = 20

# Set diameters
PHDcoll.setdiameter(25)
PHDha.setdiameter(25)
# Set Flow Rates
PHDcoll.setflowrate(flowRate)
PHDha.setflowrate(flowRate)
# Set each target volume for each infuse.
PHDcoll.settargetvolume(tVol)
PHDha.settargetvolume(tVol)


for i in range(0,cycles):
  push("Starting cycle" + str(i))
  PHDcoll.infuse()
  logging.info('Collagen: infusing, cycle ' + str(i))
  PHDcoll.stop()
  logging.info('Collagen: stopped infusing, cycle ' + str(i))
  PHDha.infuse()
  logging.info('HAnp: infusing, cycle ' + str(i))
  PHDha.stop()
  logging.info('HAnp: stopped infusing, cycle ' + str(i))

sys.exit()
