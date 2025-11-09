# liturgy.py
# The goal is to make this script print two things:
# 1. The current liturgical season
# 2. The current feast day, if it is a feast day

import datetime

# currentDate = datetime.datetime.now()
currentDate = datetime.datetime(2027, 1, 1)
currentYear = int(currentDate.strftime("%Y"))

# https://www.iccec.org/prayerandreadings/Seasons/index.php
# Determine the season. The basic Rules:
# If today is between the first day of Advent (inclusive) and Christmas, it's Advent
# If today is between Christmas (inclusive) and Epiphany (exclusive), it's Christmas
# If today is between Epiphany (inclusive) and Ash Wednesday (exclusive), it's Epiphany
# If today is between Ash Wednesday (inclusive) and Palm Sunday (exclusive), it's Lent
# If today is between Palm Sunday (inclusive) and Easter (exclusive), it's Holy Week
# If today is between Easter (inclusive) and Pentecost (exclusive), it's Easter
# If today is between Pentecost (inclusive) and Trinity Sunday (exclusive), it's Pentecost
# If today is between Trinity Sunday (inclusive) and the first day of Advent, it's Ordinary Time

# Set feast dates
feastDict  = {
	datetime.date(currentYear, 12, 24): "Christmas Eve",
	datetime.date(currentYear, 12, 25): "Christmas Day",
	datetime.date(currentYear, 1, 6): "The Epiphany"
}

# Find a feast date (key) in a dictionary by name (value)
def findFeast(dict, searchName):
	for date, name in dict.items():
		if name == searchName:
			return date

def getAdventDates():
	christmas = findFeast(feastDict, "Christmas Day")
	idx = (christmas.weekday() + 1) % 7

	firstSunday = christmas - datetime.timedelta(days = idx, weeks = 3)
	secondSunday = christmas - datetime.timedelta(days = idx, weeks = 2)
	thirdSunday = christmas - datetime.timedelta(days = idx, weeks = 1)
	fourthSunday = christmas - datetime.timedelta(days = idx)

	advent = {
		firstSunday: "First Sunday of Advent",
		secondSunday: "Second Sunday of Advent",
		thirdSunday: "Third Sunday of Advent",
		fourthSunday: "Fourth Sunday of Advent"
	}

	return advent

def getEasterDate():

	# As calculated in the 1662 Book of Common Prayer
	goldenNumber = (currentYear + 1) % 19

	# A table of golden numbers to find Easter Day taken from the 1662 Book of Common Prayer
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

	# The date of the Paschal full moon for the year
	paschal = easterDict[goldenNumber]

	# If the Paschal moon falls on a Sunday, Easter is the following Sunday
	if(paschal.weekday() + 1 == 7):
		easterDate = paschal + datetime.timedelta(days = 7)
	else:
		timeDelta = 7 - (paschal.weekday() + 1)
		easterDate = paschal + datetime.timedelta(days = timeDelta)

	return easterDate

christmas = findFeast(feastDict, "Christmas Day")
epiphany = findFeast(feastDict, "The Epiphany")
easter = getEasterDate()

print(christmas)
print(easter)


# TODO: Determine movable feasts based on easterDate

# advent = getAdventDates()

# print(list(advent)[0]) # Prints the value based on the index from the advent dictionary

# This will get the date of the feast based on the value name
# first = findFeast(advent, "First Sunday of Advent")
# print(first)
