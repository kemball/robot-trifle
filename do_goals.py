from stockings import parse_goals,parse_state,accomplish_goals,setup_robot
from opentrons import robot
import sys


if len(sys.argv)==3:
	goals = parse_goals(sys.argv[1])
	state = parse_state(sys.argv[2])
	
	with setup_robot() as robot:	
		accomplish_goals(goals,state,robot)
		print("%s commands queued" % len(robot.commands()))
		robot.run(True)
else:
	print(" please call me like %s goalfile.csv statefile.yaml"%sys.argv[0])