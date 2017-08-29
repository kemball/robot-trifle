import yaml
import sys
import csv
from collections import defaultdict



example_layout ={
	#name uL, M
	"compounds":{
		"A1":("niacin",200,5),
		"A2":("biotin",200,500),
		"A3":("niacin",200,5)
	},
	"sleepy":{
		"A1":("glucose",200,5),
		"A2":("glucose",200,5),
		"A3":("water",200,66)
	}
}


example_media = {
	"niacin":.1,
	"biotin":.2,
	"glucose":.01
}

ex_goal={
	"wells":96,
	"vol":200,
	"name":"destination",
	"excess":"water"
}

def offset_name(offset):
	letters = "ABCDEFGH"
	offset = offset%96
	fp = letters[offset%8]
	lp = int((offset)/8+1)
	return "%s%s"%(fp,lp)


def parse_layout(layfile):
	with open(layfile,'r') as lfile:
		layout = yaml.load(lfile)
	return layout
	# this should check for compatibility with a bunch of stuff
	# does the layout file have insane volumes
	# how much is there supposed to be?

def leave_one_out(goal=ex_goal,media=example_media):


	dest_wellnames = [goal["name"]+"."+offset_name(i) for i in range(0,goal["wells"])]
	spec_dict = {dw:{} for dw in dest_wellnames}
	sorted_cpds = sorted(media.keys())
	sorted_wells = sorted(dest_wellnames)
	num_replicates = int(goal["wells"]/len(sorted_cpds))

	for i,cpd in enumerate(sorted_cpds):
		for j,wn in enumerate(sorted_wells):
			if (j<num_replicates*i) or (j>= num_replicates*(i+1)):
				spec_dict[wn][cpd]=media[cpd]
	return spec_dict

def flatten(plan,layout):
	totals = defaultdict(int)
	locations = defaultdict(list)
	for container in layout.keys():
		for well,contents in layout[container].items():
			totals[contents[0]]+=contents[1]*contents[2]
			locations[contents[0]].append((
				container+"."+well,
				contents[1],
				contents[2]))
	
	def get_from_locations(cpd,moles,locations):
		for i,loc in enumerate(locations[cpd]):
			source,volume,molarity = loc
			if volume*molarity>= moles:
				amt = moles/molarity
				nt = (source,volume-amt,molarity)
				#i have to do it this way because tuples are immutable.
				locations[cpd][i] = nt
				return(source,amt)
		print("not enough %s " % cpd)

	

def layout_CDM(layout,goal=ex_goal,media=example_media,filename="goals.csv"):
	
	def get_from_locations(cpd,moles,locations):
		for i,loc in enumerate(locations[cpd]):
			source,volume,molarity = loc
			if volume*molarity>= moles:
				amt = moles/molarity
				nt = (source,volume-amt,molarity)
				#i have to do it this way because tuples are immutable.
				locations[cpd][i] = nt
				return(source,amt)
		print("not enough %s " % cpd)

	totals = defaultdict(int)
	locations = defaultdict(list)
	for container in layout.keys():
		for well,contents in layout[container].items():
			totals[contents[0]]+=contents[1]*contents[2]
			locations[contents[0]].append((
				container+"."+well,
				contents[1],
				contents[2]))
	num_cpds = len(media.keys())
	num_replicates = int(ex_goal["wells"]/num_cpds)
	#TODO: check for concentration problems
	#like the compounds are too dilute
	for compound in totals.keys():
		reqd = media[compound]*(num_cpds-1)*num_replicates*goal["vol"]
		have = totals[compound]
		if reqd>have:
			raise Exception("not enough %s, I need %s umol and I have %s umol"%(compound,reqd,have))
	
		
	matrix = [{"wellname":goal["name"]+"."+offset_name(i)} for i in range(0,goal["wells"])]

	sorted_cpds = sorted(media.keys())
	allsources = ["wellname"]
	for i,row in enumerate(matrix):
		for j,cpd in enumerate(sorted_cpds):
			#ugh here it is. This needs to be rewritten to take/make a big fat dictionary
			# a1: "glucose":.1
			#     "salt":.2
			#     "water": to 200 uL
			if (i<num_replicates*j) or (i>= num_replicates*(j+1)):
				mols = media[cpd]*goal["vol"]
				(source,amount) = get_from_locations(cpd,mols,locations)
				row[source]=amount
				if source not in allsources:
					allsources.append(source)

	with open(filename,'w') as goalfilep:
		cwriter = csv.DictWriter(goalfilep,allsources,restval=0)
		cwriter.writeheader()
		for r in matrix:
			cwriter.writerow(r)



if __name__=="__main__":
	print(yaml.dump(leave_one_out()))
	#layout_CDM(example_layout)




	






