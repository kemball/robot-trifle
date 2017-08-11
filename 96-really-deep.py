from opentrons import containers

containers.create(
	'96-really-deep',
	grid=(8,12),
	spacing=(9,9),
	depth=39,
	diameter=9,
	volume=2000)