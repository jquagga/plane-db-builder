#!/usr/bin/env python

import pandas as pd

# infile is the supplments, data to be added
infile = pd.read_csv("in.csv", header=0, dtype=str, index_col="$ICAO")

# aircraft list uses a ; instead of a comma
aircraftlist = pd.read_csv(
    "aircraft.csv.gz",
    sep=";",
    names=[
        "$ICAO",
        "$Registration",
        "$ICAO Type",
        "Zeros",
        "$Type",
        "Six",
        "$Operator",
        "Eight",
        "Nine",
    ],
    header=None,
    dtype=str,
    # index_col="0",
).set_index("$ICAO")
aircraftlist = aircraftlist.drop(["Zeros", "Six", "Eight", "Nine"], axis=1)

infile.update(aircraftlist)
# infile.to_csv("out.csv")

originaldb = pd.read_csv("plane-alert-db.csv", header=0, dtype=str, index_col="$ICAO")

# By Category; everything in category
# Note backticks `` are the secret to spaces in the column name
dictators = originaldb.query('Category == "Dictator Alert"')
gasbags = originaldb.query('Category == "Gas Bags"')
aero = originaldb.query('Category == "Aerobatic Teams"')
radiohead = originaldb.query('Category == "Radiohead"')
gov = originaldb.query('Category == "Governments"')
historic = originaldb.query('Category == "Historic"')

# By tag; same idea
# See the backticks on `$Tag 1`
# Figure out Tag 2, 3.  The # causes issues.
big = originaldb.query('`$Tag 1` == "Absolute Unit"')

# We can also add data from the aircraft.csv.gz
cool = aircraftlist.query(
    '`$ICAO Type` == ["P51","B17","B25","B29","B52","B1","A1","A6", \
    "F35","F15","F16","F18S","F18H","P38"]'
)

customdb = pd.concat(
    [infile, dictators, gasbags, aero, radiohead, gov, historic, big, cool]
)
customdb = customdb.sort_values(by="$ICAO")
customdb.to_csv("out.csv")

# For HTML, drop the tags, categories and links
htmldb = customdb.drop(
    ["#CMPG", "$Tag 1", "$#Tag 2", "$#Tag 3", "Category", "$#Link"], axis=1
)
htmldb.to_html("out.html")

# Finally let's output planes.csv which is just the ICACO
planesdb = htmldb.drop(["$Registration", "$Operator", "$Type", "$ICAO Type"], axis=1)
# add an empty column so we have a , separator
planesdb["Blank"] = ""
planesdb.to_csv("planes.csv")
