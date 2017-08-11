import json



def merge(a,b):
	c = {}
	if a==b:
		return a
	elif type(b)!=type({}):
		return b
	for key in a.keys():
		if key in b.keys():
			if b[key]==a[key]:
				c[key]=b[key]
			else:
				c[key]=merge(a[key],b[key])
		else:
			c[key]=a[key]
	for key in b.keys():
		if key not in a:
			c[key]=b[key]
	return c

if __name__=="__main__":
	import sys
	if len(sys.argv)>2:
		with open(sys.argv[1]) as oldfile:
			oj = json.load(oldfile)
		with open(sys.argv[2]) as newfile:
			nj = json.load(newfile)
		bj = merge(oj,nj)
		with open("test.json",'w') as tfile:
			json.dump(bj,tfile,indent=1)