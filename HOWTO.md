###notes on calibrations
	There's a script on pippin designed to merge two calibrations files and produce a third that contains all the entries from either file, and update conflicting entries. It calls merge_json.py, but it's not actually in the git repo.

##Bartender

The bartender code creates goals.csv files and state.yaml files. In the near future(#TODO) it will use media definitions and experimental specifications from a file.

For a complete bartender, do './bartender goal.yaml media.yaml layout.yaml' and your goals will be in goals.csv

If you want to just input a dictionary of specifications, there's a function plan_to_goals that'll do that for you. Calling it is your responsibility for now.

## walkthrough

usage: branch_and_bound.py knowns.yaml media.yaml

This will create 'new_proposed.yaml', which contains the new experiments branch_and_bound have found.

usage:bartender.py new_proposals.yaml media.yaml goal.yaml layout.yaml

this will create 'goals.csv' which contains all the concentrations and where they should go.

usage: do_goals.py goals.csv statefile.yaml

This will execute your goals on the robot.
