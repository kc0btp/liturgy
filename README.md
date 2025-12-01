# About

Liturgy is a simple python script that will calculate all of the holy days of the liturgical calendar. The goal of this project is to display the current liturgical period or holiday for the current date in [dmenu](https://tools.suckless.org/dmenu/), but it can be used as a stand-alone script as well. The primary source for my calculation has been the 1662 Anglican Book of Common Prayer, though I am not Anglican and the audience for this is not any specific denomination.

# Use

Basic use is as easy as `python liturgy.py`, which will output all of the holidays for the current year. Liturgy will also accept the `--year` or `-y` option followed by a year to list the holidays of the specified year, e.g.:

`python liturgy.py -y 2050`

# Planned Improvements

I intend to add another option to only return the date for a specified holiday, and will add a mode to only show the next, upcoming holiday relative to the current date. Eventually, I'll also have it determine the current liturgical season (e.g. Advent, Ordinary Time, etc.) based on the current date. If the current date is a holiday, the holiday name will be returned instead of the season.
