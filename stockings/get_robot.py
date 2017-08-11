from opentrons import Robot
from stockings.default_layout import *
from contextlib import contextmanager


list_of_ports = [
	"/dev/tty.usbmodem1421",
	"/dev/ttyACM0",
	"/dev/ttyACM1"
	]

def trycon(robot,tty):
	try:
		if( robot.is_simulating()):
			robot.connect(tty)
		else:
			return
	except :
		pass

@contextmanager
def setup_robot():
	robot = Robot()
	for port in list_of_ports:
		trycon(robot,port)
	if( robot.is_simulating()):
		print("no connection made")
	else:
		robot.home()
		robot._driver.speeds['z']=1200
	for (axis,pipette) in robot.get_instruments():
		pipette.load_persisted_data()
	yield robot
	robot.disconnect()
