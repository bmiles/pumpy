import sys
import pumpy
import logging
import time
import os
# Push notification stuff

import httplib, urllib

pushover_user_key = os.environ['PUSHOVER_USER_KEY']
pushover_app_key = os.environ['PUSHOVER_PUMPY_APP_TOKEN']

# Pusher
def push(message):
  conn = httplib.HTTPSConnection("api.pushover.net:443")
  conn.request("POST", "/1/messages.json",
    urllib.urlencode({
      "token": pushover_app_key,
      "user": pushover_user_key,
      "message": message,
    }), { "Content-type": "application/x-www-form-urlencoded" })
  conn.getresponse()


logging.basicConfig(level=logging.INFO)

chain = pumpy.Chain('../../../../../dev/ttyUSB0')
bufferPump = pumpy.PHD2000(chain,address=1, name="Buffer") # PHD2000
dosePump = pumpy.PHD2000(chain,address=12, name="Dose") # special pump


#Experimental Setup
#Set flow rate for whole experiment
globalFlowRate = 100

doseList = [0.00,10.00,20.00,30.00,40.00,50.00,60.00,70.00,80.00,90.00,100.00]

# Set diameters BD plastpak 10mL
bufferPump.setdiameter(14.5)
dosePump.setdiameter(14.5)

# accepts a percent of the flow as a dosing, and how long one wants to dose for.
def doseIt(dose, doseTime):
    # blank condition
    if dose == 0:
        bufferPump.setflowrate(((100.00-dose)/100.00) * globalFlowRate)

        bufferPump.infuse()

        logging.info('Infusion started at ' + str(dose)) #+ 'percent dose for ' str((doseTime/60)) +'minutes...')
        time.sleep( doseTime )

        bufferPump.stop()
        logging.info('Infusion finished at ' + str(dose)) #+ 'percent dose for ' str((doseTime/60)) +'minutes...')
    else:
        bufferPump.setflowrate(((100.00-dose)/100.00) * globalFlowRate)
        dosePump.setflowrate((dose/100.00) * globalFlowRate)

        bufferPump.infuse()
        dosePump.infuse()

        logging.info('Infusion started at ' + str(dose)) #+ 'percent dose for ' str((doseTime/60)) +'minutes...')
        time.sleep( doseTime )

        bufferPump.stop()
        dosePump.stop()
        logging.info('Infusion finished at ' + str(dose)) #+ 'percent dose for ' str((doseTime/60)) +'minutes...')

#iterates through a list of dosing percents and sens that to the infuse function.
def multiDoseIt(doses, doseTime):
    for dose in doses:
        doseIt(dose, doseTime)
        push("Started " + str(dose) + "% dose")
    return logging.info('Next!')

######## Experimental Protocol ###################
# Does a 10 minut equilibration, followed by 10 different
# doses with 5 minutes of dosing at each.

doseIt(0, 45 * 60) #single dose of buffer for 45 minutes to equilibrate
multiDoseIt(doseList, 5*60) #dose time of 5 mins
push("Job Complete :)")
sys.exit()
