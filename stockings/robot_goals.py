

import csv
from collections import defaultdict
import yaml
from opentrons import Robot
from stockings import get_from_fat_well

def parse_goals(goalfile):
	destinations= defaultdict(dict)
	with open(goalfile) as gfp:
		reader = csv.DictReader(gfp)
		for line in reader:
			dest_well_name = line["wellname"]
			#well specifiers are in format 
			#container.wellname

			for (source,amount) in line.items():
				if source=="wellname":
					continue
				else:
					destinations[source][dest_well_name]=amount
	return destinations

ex_state = {
	"compounds":{
		"A1":200,
		"A2":200,
		"A3":200
	}
}

def parse_state(statefile):
	with open(statefile) as sfp:
		deckstate = yaml.load(sfp)
	return deckstate


def accomplish_goals(goals,deckstate,robot=Robot()):
	pip = robot.get_instruments()[0][1]
	#do stuff with deckstate to set current volumes of all the wells
	for container_name in deckstate.keys():
			container_instance = robot.deck.containers()[container_name]
			for wellname in deckstate[container_name].keys():
				container_instance.wells(wellname).vol = deckstate[container_name][wellname]

	

	try:
		for source in goals.keys():
			source_container, source_well = source.split('.')
			s_well = robot.containers()[source_container].wells(source_well)
			for destination, destination_amount in goals[source].items():
				#this needs some cleverness but it'll do for now
				dest_cont,dest_well = destination.split('.')
				d_well = robot.containers()[dest_cont].wells(dest_well)
				get_from_fat_well(float(destination_amount),s_well,pip)
				pip.dispense(d_well)
				#TODO: annotate the goals somehow


	except:
		#is this a good idea?
		robot.halt() 

		for container in deckstate.keys():
			container_instance = robot.deck.containers()[container]
			#I'm really unsure about all this. IT seems wrong
			for wellname in deckstate[container].keys():
				if hasattr(container_instance.wells(wellname),"vol"):
					deckstate[container][wellname]= container_instance.wells(wellname).vol

		with open("dumpedstate.yaml",'w') as sfp:
			yaml.dump(deckstate,sfp)
		raise
