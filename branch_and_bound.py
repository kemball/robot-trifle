


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
		["glucose","niacin","NaCl","biotin","arginine","alanine","tryptophan"]
	],
	"no_growth":[
		["NaCl"]
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



def sibling_sharing(media,higher_dead_ingredients=[],oracle=lambda x: True):
	dead_ingredients=higher_dead_ingredients
	#don't modify the higher_dead_ingredients, or they'll propagate up
	if not oracle(media):
		return None
	for ing in media:
		if ing in dead_ingredients:
			continue
		smallmedia = [i for i in media if i is not ing]
		result = sibling_sharing(smallmedia,dead_ingredients,oracle)
		if not result:
			dead_ingredients.append(ing)
		else:
			return result # oh hell this is DFS
	if len(dead_ingredients)==len(media):
		#all are fatal, this is minimal
		return media

def _stupid_oracle(media):
	if "glucose" in media or "NaCl" in media and "niacin" in media:
		return True
	return False

if __name__=="__main__":
	list_media=list(example_media.keys())
	print(sibling_sharing(list_media,[],_stupid_oracle))




