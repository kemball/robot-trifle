**From the bottom up**

The last step is to actually execute the goals on the robot.

You will need(names don't matter):
	1.A goals.csv file
	2.A state.yaml file
	3.Calibrations for all the containers used (in calibrations/calibrations.json)
	4. A robot!

Both of these should be generated from bartender.

`./do_goals.py goals.csv state.yaml` from the Pi driving the robot.

**Bartender**

The bartender robot creates goals.csv files and state.yaml files. In the near future(#TODO) it will use media definitions and experimental specifications from a file.