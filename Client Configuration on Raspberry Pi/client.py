
import time
import sys
import pprint
import uuid
from uuid import getnode as get_mac

import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT) #appliance 1
GPIO.setup(7,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(11,GPIO.IN) #intruder
GPIO.setup(13,GPIO.OUT) #appliance 2
GPIO.setup(15,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(29,GPIO.OUT) #appliance 3
GPIO.setup(31,GPIO.IN,pull_up_down=GPIO.PUD_UP)
ls1='OFF'
ls2='OFF'
ls3='OFF'

try:
	import ibmiotf.application
	import ibmiotf.device
except ImportError:
	# This part is only required to run the sample from within the samples
	# directory when the module itself is not installed.
	#
	# If you have the module installed, just use "import ibmiotf.application" & "import ibmiotf.device"
	import os
	import inspect
	cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../src")))
	if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
	import ibmiotf.application
	import ibmiotf.device


def myAppEventCallback(event):
	print("Received live data from %s (%s) sent at %s: hello=%s x=%s" % (event.deviceId, event.deviceType, event.timestamp.strftime("%H:%M:%S"), data['hello'], data['x']))

def myCommandCallback(cmd):
  print("Command received: %s" % cmd.command)
  if cmd.command == "ON 1":
    print("Turning Light ON for Appliance 1")
    GPIO.output(3,1)

  elif cmd.command == "OFF 1":  
    print("Turning Light OFF for Appliance 1")
    GPIO.output(3,0) 
  
  elif cmd.command == "ON 2":
    print("Turning Light ON for Appliacne 2")
    GPIO.output(13,1)

  elif cmd.command == "OFF 2":
    print("Turning Light OFF for Appliance 2")
    GPIO.output(13,0)

  elif cmd.command == "ON 3":
    print("Turning Light ON for Appliance 3")
    GPIO.output(29,1)

  elif cmd.command == "OFF 3":
    print("Turning Light OFF for Appliance 3")
    GPIO.output(29,0)
    
#####################################
#FILL IN THESE DETAILS
#####################################     
# organization = "ovil5l"
# deviceType = "raspberry_pi"
# deviceId = "b827eb61ccaa"
# appId = str(uuid.uuid4())
# authMethod = "token"
# authToken = "V0b3bK7SalG@DsuQS*"

organization = "ysoznq"
deviceType = "raspberry_pi"
deviceId = "b827eb61ccaa"
appId = str(uuid.uuid4())
authMethod = "token"
authToken = "WrndLEBcQXFY_3o_9z"

# Initialize the device client.
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
	print(str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
deviceCli.commandCallback = myCommandCallback
#x=0
while(1):
	lightStatus1=GPIO.input(7) 
	lightStatus2=GPIO.input(13)
	lightStatus3=GPIO.input(31)
	if lightStatus1==0:
		ls1='ON'
	else:
		ls1='OFF'
	if lightStatus2==0:
		ls2='ON'
	else:	
		ls2='OFF'
	if lightStatus3==0:
		ls3='ON'
	else:
		ls3="OFF"
	data = {'Light Status 1': ls1, 'Light Status 2': ls2, 'Light Status 3': ls3}
	deviceCli.publishEvent("status","json", data)
	#x=x+1
	time.sleep(1)
		

# Disconnect the device and application from the cloud
deviceCli.disconnect()
#appCli.disconnect()

