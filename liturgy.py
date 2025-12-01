# liturgy.py
# The goal is to make this script print two things:
# 1. The current liturgical season.
# 2. The current feast day, if it is a feast day.

import argparse
import datetime
from datetime import timedelta

# Constants
DAYS_IN_WEEK = 7
feastDict = {}

parser = argparse.ArgumentParser(description='Liturgy')
parser.add_argument('-y', '--year', type=int, nargs='?', help='Display all the feasts in a specific year.')
args = parser.parse_args()

if(args.year is None):
	currentDate = datetime.datetime.now()
else:
	if args.year < 0:
		parser.error("Specified year must be greater than 0.")
	currentDate = datetime.datetime(args.year, 1, 1)

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

	feastDict.update({easterDate: "Easter"})
	return easterDate

# Ash Wednesday is always 46 days before Easter
def getAshWednesday(easterDate):
	ashWednesdayDate = easterDate + timedelta(days=-46)
	feastDict.update({ashWednesdayDate: "Ash Wednesday"})

# Palm Sunday is the Sunday before Easter
def getPalmSunday(easterDate):
	palmSundayDate = easterDate + timedelta(weeks=-1)
	feastDict.update({palmSundayDate: "Palm Sunday"})

# NOTE: This entire main() function is currently for development only
# TODO: Replace this with something that only outputs info relevant to today by default
def main():

	easterDate = getEasterDate()

	getAshWednesday(easterDate)
	getPalmSunday(easterDate)
	getAdventDates()

	# Print out all the values for now:
	for(date, name) in sorted(feastDict.items()):
		print(f"{name}: {date}")

if __name__ == "__main__":
	main()

# TODO: Calculate Pentecost
# TODO: Calculate Trinity Sunday
# TODO: Determine Ordinary Time
# TODO: Create a "print" function that handles the logic of formatting and adjusting date based on whether this year's feast has already passed.
# REFACTOR: Figure out a way to determine current holiday season based on today's date
# REFACTOR: findFeast should be able to get current year feast but also next occurrence of a feast even if it's in the next year. Maybe findFeast can remain a pure function to find the feasts within a given year, but then I make a separate function that I can use to determine whether the feast date has already occurred and adjust the year accordingly.