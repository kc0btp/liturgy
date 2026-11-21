#!/usr/bin/env python3
"""Simple liturgical season/holiday detector for the Western Christian calendar.

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
    1: (4, 14),
    2: (4, 3),
    3: (3, 23),
    4: (4, 11),
    5: (3, 31),
    6: (4, 18),
    7: (4, 14),
    8: (4, 8),
    9: (4, 16),
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


def easter_date(year: int) -> date:
    """Calculate Easter Sunday using the 1662 BCP Paschal Moon table."""
    golden_number = (year % 19) + 1
    month, day = PASCHAL_MOON_DATES[golden_number]
    paschal_moon = date(year, month, day)

    if paschal_moon.weekday() == 6:
        return paschal_moon + timedelta(days=7)

    days_until_sunday = 7 - (paschal_moon.weekday() + 1)
    return paschal_moon + timedelta(days=days_until_sunday)


def advent_start(year: int) -> date:
    """Advent starts on the fourth Sunday before Christmas, i.e. the Sunday between Nov 27 and Dec 3 inclusive."""
    # search Nov 27..Dec 3 for Sunday
    for day in range(27, 31):
        try_date = date(year, 11, day)
        if try_date.weekday() == 6:  # Sunday
            return try_date
    # fallback: search Dec 1..Dec 3
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


def detect_liturgical_season(d: date) -> str:
    y = d.year
    today = d

    # Easter and related movable feasts
    easter = easter_date(y)
    ash = easter - timedelta(days=46)
    palm = easter - timedelta(days=7)
    holy_thursday = easter - timedelta(days=3)
    good_friday = easter - timedelta(days=2)
    holy_saturday = easter - timedelta(days=1)
    ascension = easter + timedelta(days=39)
    pentecost = easter + timedelta(days=49)

    # Advent (starts in late Nov/early Dec)
    adv_start = advent_start(y)
    adv_end = date(y, 12, 24)

    # Christmas: Dec 25 -> Jan 5 (approx. until Epiphany)
    christ_start = date(y, 12, 25)
    christ_end = date(y + 1, 1, 5)

    # If date is in early January, treat Christmas season of previous year
    if d.month == 1 and d.day <= 5:
        christ_start = date(y - 1, 12, 25)
        christ_end = date(y, 1, 5)

    # Ordinary Time ranges (approximated)
    ordinary_winter_start = date(y, 1, 6)
    ordinary_winter_end = ash - timedelta(days=1)

    ordinary_summer_start = pentecost + timedelta(days=1)
    ordinary_summer_end = adv_start - timedelta(days=1)

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
        return "Ascension (observed)"
    if d == pentecost:
        return "Pentecost"

    # Seasons
    if adv_start <= d <= adv_end:
        if d.weekday() == 6:
            return advent_sunday_name(d, adv_start)
        return "Advent"

    # Christmas season (covers Jan 1..Jan 5 or Dec 25..Dec31)
    if christ_start <= d <= christ_end:
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
