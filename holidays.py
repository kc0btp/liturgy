import datetime

currentYear = int(datetime.date.today().strftime("%Y"))

def easter():
	easterDict = { # A table to find easter day taken from the 1662 Book of Common Prayer
		1: datetime.date(currentYear, 4, 14),
		2: datetime.date(currentYear, 4, 3),
		3: datetime.date(currentYear, 3, 23),
		11: datetime.date(currentYear, 3, 25),
		14: datetime.date(currentYear, 3, 21)
	}

	goldenNumber = (currentYear + 1) % 19
	easterDate = easterDict[goldenNumber]
	# print(easterDate.strftime("%B") + " " + easterDate.strftime("%d"))

	return easterDate

if(datetime.date.today() == easter()):
	print("It's Easter")
else:
	print("It's not Easter")