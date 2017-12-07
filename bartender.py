import yaml
import csv
from collections import defaultdict
from io import StringIO



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
		"A3":("glucose",5000,5),
		"A3":("water",200,66)
	},
	"dopey":{
		"A1":("NaCl",200,1),
		"A2":("alanine",200,1),
		"A3":("arginine",200,1),
		"A4":("tryptophan",200,1)
	}
}

def convert_layout_to_state(layout):
	state = {}
	for key,value in layout.items():
		state[key] = value
	for _,value in state.items():
		for k,v in value.items():
			value[k] = v[1]
	return state

example_media = {
	"glucose":1,
	"niacin":.01,
	"NaCl":.01,
	"biotin":.0005,
	"alanine":.002,
	"arginine":.005,
	"tryptophan":.00015,
}

ex_goal={
	"wells":96,
	"vol":10, #in umol
	"name":"destination",
	"excess":"water"
}

def offset_name(offset):
	letters = "ABCDEFGH"
	offset = offset%96
	fp = letters[offset%8]
	lp = int((offset)/8+1)
	return "%s%s"%(fp,lp)

def _generic_parse_yaml(file):
	with open(file,'r') as fo:
		return yaml.load(fo)


def parse_layout(layfile):
	with open(layfile,'r') as lfile:
		layout = yaml.load(lfile)
	return layout
	# this should check for compatibility with a bunch of stuff
	# does the layout file have insane volumes

parse_plan = _generic_parse_yaml

parse_goal = _generic_parse_yaml

parse_media = _generic_parse_yaml

parse_proposals = _generic_parse_yaml
#renaming functions 

def leave_one_out(goal=ex_goal,media=example_media):

	#do concentration here.
	dest_wellnames = [goal["name"]+"."+offset_name(i) for i in range(0,goal["wells"])]
	spec_dict = {dw:{} for dw in dest_wellnames}
	sorted_cpds = sorted(media.keys())
	sorted_wells = sorted(dest_wellnames)
	num_replicates = int(goal["wells"]/len(sorted_cpds))

	for i,cpd in enumerate(sorted_cpds):
		for j,wn in enumerate(sorted_wells):
			if (j<num_replicates*i) or (j>= num_replicates*(i+1)):
				spec_dict[wn][cpd]=media[cpd]*goal["vol"]#in umols
	return spec_dict #'plan'

def proposals(proposed =[],media=example_media,goal=ex_goal):
	dest_wellnames = [goal["name"]+"."+offset_name(i) for i in range(0,goal["wells"])]
	sorted_wells = sorted(dest_wellnames)
	num_replicates = int(goal["wells"]/len(proposed))
	spec_dict = {dw:{} for dw in dest_wellnames}
	for i,prop in enumerate(proposed):
		for j,wn in enumerate(sorted_wells):
			if (j<num_replicates*i) or (j>= num_replicates*(i+1)):
				for cpd in prop:
					spec_dict[wn][cpd]=media[cpd]*goal["vol"]#in umols	
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
	
	
	def get_from_locations(cpd,umoles,locations):
		for i,loc in enumerate(locations[cpd]):
			source,volume,molarity = loc
			if volume*molarity>= umoles:
				amt = umoles/molarity
				nt = (source,volume-amt,molarity)
				#i have to do it this way because tuples are immutable.
				locations[cpd][i] = nt
				return(source,amt)
		raise Exception("I won't pool the last little bits of this. I need more %s" %compound)

	matrix = [{"wellname":k} for k in plan.keys()]
	allsources=["wellname"]
	for m in matrix:
		ingredients = plan[m["wellname"]]
		for ing,umols in ingredients.items():
			totals[ing]-=umols
			if totals[ing]<0:
				raise Exception("Not enough %s to complete a transfer spreadsheet." % ing)
			(source,amt) = get_from_locations(ing,umols,locations)
			if source not in allsources:
				allsources.append(source)
			m[source]=amt
	return(matrix,allsources)

def write_to_file(matrix,allsources,file):
	with open(file,'w') as fakefile:

		cwriter = csv.DictWriter(fakefile,allsources,restval=0)
		cwriter.writeheader()
		for line in matrix:
			cwriter.writerow(line)
		
def plan_to_goals(planfile,layoutfile,output="goals.csv"):
	layout = parse_layout(layoutfile)
	plan = parse_plan(planfile)
	(m,a) = flatten(plan,layout)
	write_to_file(m,a,output)



if __name__=="__main__":
	from sys import argv
	usage = "bartender.py new_proposals.yaml media.yaml goal.yaml layout.yaml"
	if len(argv)<5:
		with open('example_goal.yaml','w') as gf:
			yaml.dump(ex_goal,gf)
		with open('example_layout.yaml','w') as lf:
			yaml.dump(example_layout,lf)
		print(usage)
	else:
		props = parse_proposals(argv[1])
		media = parse_media(argv[2])
		goal = parse_goal(argv[3])
		layout = parse_layout(argv[4])
		plan = proposals(props,media,goal)
		m,a = flatten(plan,layout)
		write_to_file(m,a,"goals.csv")
		with open('statefile.yaml','w') as sf:
			yaml.dump(convert_layout_to_state(layout),sf)
		print("goals.csv contains your new goals, and statefile.yaml contains your new board state.") 




	






