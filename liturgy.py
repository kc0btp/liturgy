import datetime

currentDate = datetime.datetime.now()
currentYear = int(currentDate.strftime("%Y"))

def getEasterDate():

	# A table to find easter day taken from the 1662 Book of Common Prayer
	easterDict = {
		1: datetime.date(currentYear, 4, 14),
		2: datetime.date(currentYear, 4, 3),
		3: datetime.date(currentYear, 3, 23),
		4: datetime.date(currentYear, 4, 11),
		5: datetime.date(currentYear, 3, 31),
		6: datetime.date(currentYear, 4, 18),
		7: datetime.date(currentYear, 4, 14),
		8: datetime.date(currentYear, 4, 8),
		9: datetime.date(currentYear, 4, 16),
		10: datetime.date(currentYear, 4, 5),
		11: datetime.date(currentYear, 3, 25),
		12: datetime.date(currentYear, 4, 13),
		13: datetime.date(currentYear, 4, 2),
		14: datetime.date(currentYear, 3, 22),
		15: datetime.date(currentYear, 4, 10),
		16: datetime.date(currentYear, 3, 30),
		17: datetime.date(currentYear, 4, 17),
		18: datetime.date(currentYear, 4, 7),
		19: datetime.date(currentYear, 3, 27)
	}

	goldenNumber = (currentYear + 1) % 19
	easterDate = easterDict[goldenNumber]

	return easterDate

# TODO: Determine movable feasts based on easterDate

# TODO: Add static date table

if(datetime.date.today() == getEasterDate()):
	print("It's Easter")
else:
	print("It's not Easter")