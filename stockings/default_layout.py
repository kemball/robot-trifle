from opentrons import Robot,containers,instruments

p200rack = containers.load(
	'tiprack-200ul',
	'A1',
	'tiprack'
)

compounds = containers.load(
    '96-really-deep',
    'B1',
    'compounds'
)

destination = containers.load(
    '96-really-deep',
    'C1',
    'destination'
)

sleepy = containers.load(
    '96-really-deep',
    'D1',
    'sleepy')

trash = containers.load(
    'point',
    'D2',
    'trash'
)


p200 = instruments.Pipette(
    name="p200",
    axis="b",
    min_volume=20,
    max_volume=200,
    tip_racks=[p200rack],
    trash_container=trash,
    channels=1
)