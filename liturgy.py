#!/usr/bin/env python3

"""liturgy.py
A simple liturgical season/holiday detector for the Western Christian calendar.
The goal is to make this script print two things:
1. The current liturgical season.
2. The current feast day, if it is a feast day.

Usage:
  uv run liturgy.py                   # uses today's date
  uv run liturgy.py 2026-02-14        # use specific date
  uv run liturgy.py --debug           # includes the date
  uv run liturgy.py 2026-02-14 --debug
"""

from __future__ import annotations
import sys
from datetime import date, timedelta

PASCHAL_MOON_DATES = {
    1:  (4, 14),
    2:  (4, 3),
    3:  (3, 23),
    4:  (4, 11),
    5:  (3, 31),
    6:  (4, 18),
    7:  (4, 14),
    8:  (4, 8),
    9:  (4, 16),
    10: (4, 5),
    11: (3, 25),
    12: (4, 13),
    13: (4, 2),
    14: (3, 22),
    15: (4, 10),
    16: (3, 30),
    17: (4, 17),
    18: (4, 7),
    19: (3, 27),
}

# Calculate Easter Sunday using the 1662 BCP Paschal Moon table.
def easter_date(year: int) -> date:
    golden_number = (year % 19) + 1
    month, day = PASCHAL_MOON_DATES[golden_number]
    paschal_moon = date(year, month, day)

    if paschal_moon.weekday() == 6:
        return paschal_moon + timedelta(days=7)

    days_until_sunday = 7 - (paschal_moon.weekday() + 1)
    return paschal_moon + timedelta(days = days_until_sunday)

# Advent starts on the fourth Sunday before Christmas.
# Find the first Sunday between Nov 27 and Dec 3 inclusive.
def advent_start(year: int) -> date:
    # Search Nov 27..Dec 3 for Sunday
    for day in range(27, 31):
        try_date = date(year, 11, day)
        if try_date.weekday() == 6:  # Sunday
            return try_date
    # Fallback: search Dec 1..Dec 3
    for day in range(1, 4):
        try_date = date(year, 12, day)
        if try_date.weekday() == 6:
            return try_date
    return date(year, 11, 27)

def advent_sunday_name(d: date, adv_start: date) -> str:
    """Return the numbered name for an Advent Sunday."""
    week = (d - adv_start).days // 7 + 1
    ordinals = ("First", "Second", "Third", "Fourth")
    if 1 <= week <= len(ordinals):
        return f"{ordinals[week - 1]} Sunday of Advent"
    return "Advent"

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

def detect_liturgical_season(d: date) -> str:
    y = d.year
    today = d

    # Easter and related movable feasts
    easter = easter_date(y)
    ash = easter - timedelta(days = 46)
    palm = easter - timedelta(days = 7)
    holy_thursday = easter - timedelta(days = 3)
    good_friday = easter - timedelta(days = 2)
    holy_saturday = easter - timedelta(days = 1)
    ascension = easter + timedelta(days = 39)
    pentecost = easter + timedelta(days = 49)

    # Advent
    # Starts in late November/early December
    # Ends on December 24
    adv_start = advent_start(y)
    adv_end = date(y, 12, 24)

    # Christmas: Dec 25 -> Jan 5 (approx. until Epiphany)
    christmas_start = date(y, 12, 25)
    christmas_end = date(y + 1, 1, 5)

    # If date is in early January, treat Christmas season of previous year
    if d.month == 1 and d.day <= 5:
        christmas_start = date(y - 1, 12, 25)
        christmas_end = date(y, 1, 5)

    # Ordinary Time ranges (approximated)
    ordinary_winter_start = date(y, 1, 6)
    ordinary_winter_end = ash - timedelta(days = 1)

    ordinary_summer_start = pentecost + timedelta(days = 1)
    ordinary_summer_end = adv_start - timedelta(days = 1)

    # Special fixed feasts
    if d == ash:
        return "Ash Wednesday"
    if d == palm:
        return "Palm Sunday (Holy Week)"
    if d == holy_thursday:
        return "Maundy Thursday (Holy Thursday)"
    if d == good_friday:
        return "Good Friday"
    if d == holy_saturday:
        return "Holy Saturday"
    if d == easter:
        return "Easter Sunday"
    if d == ascension:
        return "Ascension"
    if d == pentecost:
        return "Pentecost"
    if d.month == 12 and d.day == 24:
        return "Christmas Eve"
    if d.month == 12 and d.day == 25:
        return "Christmas Day"

    # Seasons
    if adv_start <= d <= adv_end:
        if d.weekday() == 6:
            return advent_sunday_name(d, adv_start)
        return "Advent"

    # Christmas season (covers Jan 1..Jan 5 or Dec 25..Dec31)
    if christmas_start <= d <= christmas_end:
        return "Christmas Season"

    # Epiphany (Jan 6)
    if d.month == 1 and d.day == 6:
        return "Epiphany"

    # Lent (from Ash Wednesday until start of Holy Week)
    if ash <= d < palm:
        return "Lent"

    # Holy Week (Palm Sunday through Holy Saturday)
    if palm <= d < easter:
        return "Holy Week"

    # Easter Season (Easter Sunday through Pentecost)
    if easter <= d <= pentecost:
        return "Easter Season"

    # Ordinary Time (before Lent)
    if ordinary_winter_start <= d <= ordinary_winter_end:
        return "Ordinary Time"

    # Ordinary Time (after Pentecost until Advent)
    if ordinary_summer_start <= d <= ordinary_summer_end:
        return "Ordinary Time"

    # If none matched, default to Ordinary Time
    return "Ordinary Time"

def main(argv: list[str]):
    debug = "--debug" in argv
    arguments = [argument for argument in argv[1:] if argument != "--debug"]

    if arguments:
        try:
            parts = arguments[0].split("-")
            y, m, day = map(int, parts)
            d = date(y, m, day)
        except Exception:
            print("Invalid date. Use YYYY-MM-DD")
            return 2
    else:
        d = date.today()

    season = detect_liturgical_season(d)
    print(f"{d.isoformat()}: {season}" if debug else season)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
