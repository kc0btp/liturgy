# liturgy.py
# The goal is to make this script print two things:
# 1. The current liturgical season.
# 2. The current feast day, if it is a feast day.

import datetime

# Constants
DAYS_IN_WEEK = 7
feastDict = {}

currentDate = datetime.datetime.now()
# currentDate = datetime.datetime(2027, 1, 1)
currentYear = int(currentDate.strftime("%Y"))

# https://www.iccec.org/prayerandreadings/Seasons/index.php
# Determine the season. The basic Rules:
# If today is between the first day of Advent (inclusive) and Christmas, it's Advent.
# If today is between Christmas (inclusive) and Epiphany (exclusive), it's Christmas.
# If today is between Epiphany (inclusive) and Ash Wednesday (exclusive), it's Epiphany.
# If today is between Ash Wednesday (inclusive) and Palm Sunday (exclusive), it's Lent.
# If today is between Palm Sunday (inclusive) and Easter (exclusive), it's Holy Week.
# If today is between Easter (inclusive) and Pentecost (exclusive), it's Easter.
# If today is between Pentecost (inclusive) and Trinity Sunday (exclusive), it's Pentecost.
# If today is between Trinity Sunday (inclusive) and the first day of Advent, it's Ordinary Time.

# Add fixed feast dates
feastDict.update(
	{
		datetime.date(currentYear, 12, 24): "Christmas Eve",
		datetime.date(currentYear, 12, 25): "Christmas Day",
		datetime.date(currentYear, 1, 6): "The Epiphany"
	}
)

# Generic function to find a feast date (key) in a dictionary by name (value).
def findFeast(dict, searchName):
	for date, name in dict.items():
		if name == searchName:
			return date

# Calculate the four Sundays of Advent based on the date of Christmas.
def getAdventDates():
	christmas = findFeast(feastDict, "Christmas Day")
	idx = (christmas.weekday() + 1) % DAYS_IN_WEEK # Add 1 for 0-indexed week values

	firstSunday = christmas - datetime.timedelta(days = idx, weeks = 3)
	secondSunday = christmas - datetime.timedelta(days = idx, weeks = 2)
	thirdSunday = christmas - datetime.timedelta(days = idx, weeks = 1)
	fourthSunday = christmas - datetime.timedelta(days = idx)

	feastDict.update(
		{
			firstSunday: "First Sunday of Advent",
			secondSunday: "Second Sunday of Advent",
			thirdSunday: "Third Sunday of Advent",
			fourthSunday: "Fourth Sunday of Advent"
		}
	)

# Calculate the date of Easter based on the Paschal Moon and golden numbers.
def getEasterDate():

	# A table of golden numbers to find Easter Day taken from the 1662 Book of Common Prayer.
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

	# Calculate the year's golden number per the 1662 Book of Common Prayer.
	goldenNumber = (currentYear + 1) % len(easterDict) # Add 1 for zero-indexed week values

	# The date of the Paschal full moon for the year.
	paschal = easterDict[goldenNumber]

	# The Sunday following the Paschal moon.
	# If the Paschal moon falls on a Sunday, Easter is the following Sunday.
	if(paschal.weekday() + 1 == DAYS_IN_WEEK):
		easterDate = paschal + datetime.timedelta(days = DAYS_IN_WEEK)
	else:
		timeDelta = DAYS_IN_WEEK - (paschal.weekday() + 1)
		easterDate = paschal + datetime.timedelta(days = timeDelta)

	feastDict.update(
		{
			easterDate: "Easter",
		}
	)

def main():
	christmas = findFeast(feastDict, "Christmas Day")
	epiphany = findFeast(feastDict, "The Epiphany")

	getEasterDate()
	easter = findFeast(feastDict, "Easter")

	getAdventDates()
	firstSundayofAdvent = findFeast(feastDict, "First Sunday of Advent")
	secondSundayofAdvent = findFeast(feastDict, "Second Sunday of Advent")
	thirdSundayofAdvent = findFeast(feastDict, "Third Sunday of Advent")
	fourthSundayofAdvent = findFeast(feastDict, "Fourth Sunday of Advent")

	# Print out all the values for now:
	print("Christmas: " + str(christmas))
	print("Epiphany: " + str(epiphany))
	print("Easter: " + str(easter))
	print("First Sunday of Advent: " + str(firstSundayofAdvent))
	print("Second Sunday of Advent: " + str(secondSundayofAdvent))
	print("Third Sunday of Advent: " + str(thirdSundayofAdvent))
	print("Fourth Sunday of Advent: " + str(fourthSundayofAdvent))

if __name__ == "__main__":
	main()

# TODO: Calculate Ash Wednesday
# TODO: Calculate Palm Sunday
# TODO: Calculate Pentecost
# TODO: Calculate Trinity Sunday
# TODO: Determine Ordinary Time
# REFACTOR: Figure out a way to determine current holiday based on today's date