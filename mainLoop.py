#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
from stepperRobotArm import StepperRobotArm 
from replicaRobotArm import ReplicaRobotArm 
from blinkLED import BlinkLED 
from button import Button
from switch import Switch

# - - - - - - - - - - - - - - - - 
# - - - - - GPIO Setup  - - - - -
# - - - - - - - - - - - - - - - -
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)  # Replay button
GPIO.setup(16,GPIO.IN)   # Delete button 
GPIO.setup(6, GPIO.IN)   # ON switch
GPIO.setup(13, GPIO.IN)  # Unused switch
GPIO.setup(19, GPIO.IN)  # Unused switch
GPIO.setup(26, GPIO.IN)  # Follow switch
GPIO.setup(12, GPIO.IN)  # Repeat switch
GPIO.setup(21, GPIO.OUT) # Blink LED


# - - - - - - - - - - - - - - - - 
# - - -  Global Objects - - - - -
# - - - - - - - - - - - - - - - -
blinkLED = BlinkLED(21)

stepperArm = StepperRobotArm(blinkLED)
replicaArm = ReplicaRobotArm()

replayButton = Button(20, stepperArm.shortPressAction, lambda: True)
deleteButton = Button(16, stepperArm.deleteReplayList, lambda: True)

onSwitch = Switch(6, lambda: True, lambda: True)
unused1Switch = Switch(13, lambda: True, lambda: True)
setOriginSwitch = Switch(19, replicaArm.getCorrValues, lambda: True)
followSwitch = Switch(26, lambda: stepperArm.setMode('follow'), lambda: stepperArm.setMode('idle'))
repeatSwitch = Switch(12, lambda: stepperArm.setMode('replay'), lambda: stepperArm.setMode('idle'))

# - - - - - - - - - - - - - - - - 
# - - - UPDATE INPUT DEVICES  - -
# - - - - - - - - - - - - - - - -
def updateInputDevices():
    replayButton.update()
    deleteButton.update()
    onSwitch.update()
    unused1Switch.update()
    setOriginSwitch.update()
    followSwitch.update()
    repeatSwitch.update()

# - - - - - - - - - - - - - - - - 
# - -  UPDATE OUTPUT DEVICES  - -
# - - - - - - - - - - - - - - - -
def updateOutputDevices():
    blinkLED.update()

# - - - - - - - - - - - - - - - - 
# - - - - UPDATE ROBOT ARM  - - -
# - - - - - - - - - - - - - - - -
def updateRobotArm():
    if stepperArm.checkIfIdle():
        if stepperArm.mode is 'follow':
            stepperArm.moveToPosition(replicaArm.posDict)
        elif stepperArm.mode is 'replay':
            if stepperArm.replayStepList:
                blinkLED.setMode('slowBlink')
                reciever, command = stepperArm.replayStepList.pop(0)
                print(reciever, command)
                if reciever is 'arm':
                    stepperArm.moveToPositionRaw(command)
            else:
                blinkLED.setMode('idle')

# - - - - - - - - - - - - - - - - 
# - - - - - MAIN LOOP - - - - - -
# - - - - - - - - - - - - - - - -
while True:
    updateInputDevices()
    updateOutputDevices()
    replicaArm.update()
    updateRobotArm()
    time.sleep(0.1)
