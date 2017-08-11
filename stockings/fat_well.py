
def get_from_fat_well(amount,well,pipette):
	if not hasattr(well,"vol"):
		well.vol = well.max_volume()
	(w,top) = well.top()
	(x,bot) = well.bottom()
	z = (top-bot)*(.8*(well.vol-amount)/(well.max_volume()))
	z -= (0,0,5) #5 mm below apparent surface
	z += bot
	if z[2]<bot[2]:
		z=bot
	pipette.aspirate(amount,(well,z))
	well.vol -= amount
	if well.vol <0:
		print("Warning: well %s is probably empty" %repr(well))
		well.vol=0

def airgap_train(batch,amt,airgap,well,p200):
	for a in batch:
		get_from_fat_well(amt,well,p200)
		if a is not batch[-1]:
			p200.air_gap(airgap)