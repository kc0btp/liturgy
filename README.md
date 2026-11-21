# About

Liturgy is a simple python script that will calculate the holy days of the liturgical calendar. The goal of this project is to display the current liturgical period or holiday for the current date in the macOS menu bar with [SwiftBar](https://github.com/swiftbar/SwiftBar), but it can be used as a stand-alone script as well. The primary source for my calculation has been the 1662 Anglican Book of Common Prayer, though I am not Anglican and the audience for this is not any specific denomination.

Full disclosure: I am a mere hobbyist. I started writing this myself and lost interest after a while, but now that all the cool kids are using AI, I decided to try my hand at some basic vibe coding. This is the result.

# Output examples

- `2026-04-05: Palm Sunday (Holy Week)`
- `2026-04-12: Easter Sunday`
- `2026-12-06: Second Sunday of Advent`
- `2026-12-07: Advent`

# Setup

This project uses [uv](https://docs.astral.sh/uv/) to manage Python and dependencies.

```bash
uv sync
```

# Use

Run for today:

```bash
uv run liturgy.py
```

Run for a specific date (YYYY-MM-DD):

```bash
uv run liturgy.py 2026-04-05
```

Debug output includes the date:

```bash
uv run liturgy.py --debug
uv run liturgy.py 2026-04-05 --debug
```

# Planned Improvements

I intend to add another option to only return the date for a specified holiday, and will add a mode to only show the next, upcoming holiday relative to the current date. Eventually, I'll also have it determine the current liturgical season (e.g. Advent, Ordinary Time, etc.) based on the current date. If the current date is a holiday, the holiday name will be returned instead of the season.
