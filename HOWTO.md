**From the bottom up**

The last step is to actually execute the goals on the robot.

You will need(names don't matter):
	1.A goals.csv file
	2.A state.yaml file
	3.Calibrations for all the containers used (in calibrations/calibrations.json)
	4. A robot!

Both of these should be generated from bartender.

`./do_goals.py goals.csv state.yaml` from the Pi driving the robot.

*notes on calibrations*
	There's a script on pippin designed to merge two calibrations files and produce a third that contains all the entries from either file, and update conflicting entries. It calls merge_json.py, but it's not actually in the git repo.

**Bartender**

The bartender robot creates goals.csv files and state.yaml files. In the near future(#TODO) it will use media definitions and experimental specifications from a file.

It's called like `./bartender.py media.yaml experiment.yaml`