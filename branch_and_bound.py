


example_media = {
	"glucose":1,
	"niacin":.01,
	"NaCl":.01,
	"biotin":.0005,
	"alanine":.002,
	"arginine":.005,
	"tryptophan":.00015,
}


example_knowns = {
	"growth":[
		set(["glucose","niacin","NaCl","biotin","arginine","alanine","tryptophan"])
	],
	"no_growth":[
		set(["NaCl"])
	]
}

def BFS(knowns=example_knowns,media=example_media):
	def return_smallest(media,oracle):
		if not oracle(media):
			return None
		children = []
		for ing in media:
			smallmedia = [i for i in media if i is not ing]
			children.append(return_smallest(smallmedia,oracle))
		good_children = [child for child in children if child]
		if len(good_children)==0:
			return media
		else:
			best = min(map(len,good_children))
			for child in good_children:
				if len(child)==best:
					return child
			print("could not find the smallest child. That is perplexing.")
	return return_smallest(media)
	#something involving currying has to go here
	# but that's a story for a different day



def sibling_sharing(media,dead_ingredients=[],oracle=lambda x: len(x)>0):
	#media is a set()
	solutions = []
	for ing in media:
		if ing in dead_ingredients:
			continue
		smallmedia = set([i for i in media if i is not ing])
		result = oracle(smallmedia)
		if not result:
			dead_ingredients.append(ing)
		else:
			# the full slice [:] copies the list.
			new_sol = sibling_sharing(smallmedia,dead_ingredients[:],oracle)
			for sol in new_sol:
				if sol not in solutions:
					solutions.append(sol)
	if len(solutions)==0:
		#all are fatal, this is minimal
		return [media]
	#minimal_size = min(map(len,solutions))
	return solutions


def _stupid_oracle(media):
	if( "NaCl" in media) and ("niacin" in media or "glucose" in media):
		return True
	if ("biotin" in media):
		return True
	return False

def oracle(media, knowns, proposed):
	if media in knowns["no_growth"]:
		return False
	elif media in knowns["growth"]:
		return True
	else:
		proposed.append(media)
		return False

from functools import partial

if __name__=="__main__":
	from sys import argv
	import yaml

	if len(argv)<2:
		print("usage: branch_and_bound.py knowns.yaml media.yaml")
		list_media=set(list(example_media.keys()))
		print("full: ",list_media)
		proposals = []
		known_oracle = partial(oracle,knowns=example_knowns,proposed=proposals)
		print("minimal ",sibling_sharing(list_media,[],known_oracle))
		with open("example_media.yaml",'w') as yf:
			yaml.dump(example_media,yf)
		with open("example_knowns.yaml",'w') as yf:
			yaml.dump(example_knowns,yf)
		with open("example_proposed.yaml","w") as pf:
			yaml.dump(proposals,pf)
		print("proposed: ", "\n".join(map(str,proposals)))
	else:
		with open(argv[1],'r') as kf:
			knowns = yaml.load(kf)
		with open(argv[2],'r') as mf:
			media = yaml.load(mf)
		list_media = set(list(media.keys()))
		proposals = []
		known_oracle = partial(oracle,knowns=knowns,proposed=proposals)
		print("minimal ",sibling_sharing(list_media,[],known_oracle))
		print("proposed new experiments: ",proposals)
		with open("new_proposed.yaml","w") as pf:
			yaml.dump(proposals.pf)

	#print(sibling_sharing(list_media))




