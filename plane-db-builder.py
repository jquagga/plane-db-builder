#!/usr/bin/env python

import pandas as pd

# supplement is the additional ICAOs to be added
supplement = pd.read_csv("supplement.csv", header=0, dtype=str, index_col="$ICAO")

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

# Patch the supplement list with data from the aircraft database
supplement.update(aircraftlist)
supplement.to_csv("supplement.csv")

originaldb = pd.read_csv("plane-alert-db.csv", header=0, dtype=str, index_col="$ICAO")

# By Category; everything in category
# Note backticks `` are the secret to spaces in the column name
dictators = originaldb.query('Category == "Dictator Alert"')
gasbags = originaldb.query('Category == "Gas Bags"')
aero = originaldb.query('Category == "Aerobatic Teams"')
radiohead = originaldb.query('Category == "Radiohead"')
gov = originaldb.query('Category == "Governments"')
historic = originaldb.query('Category == "Historic"')
dbcool = originaldb.query('Category == "Joe Cool"')

# By tag; same idea
# See the backticks on `$Tag 1`
# Figure out Tag 2, 3.  The # causes issues.
big = originaldb.query('`$Tag 1` == "Absolute Unit"')

# We can also add data from the aircraft.csv.gz
cool = aircraftlist.query(
    '`$ICAO Type` == ["P51","B17","B25","B29","B52","B1","A1","A6", \
    "F35","F15","F16","F18S","F18H","P38","AT43","AT44", \
    "AT45","AT72","SHIP","U2","P3","E6","P8","EUFI","C5M"]'
)

customdb = pd.concat(
    [supplement, dictators, gasbags, aero, radiohead, gov, historic, big, cool]
)
customdb = customdb.drop_duplicates()
customdb = customdb.sort_values(by="$ICAO")
customdb.to_csv("plane-alert-db-custom.csv")

# For HTML, drop the tags, categories and links
htmldb = customdb.drop(
    ["#CMPG", "$Tag 1", "$#Tag 2", "$#Tag 3", "Category", "$#Link"], axis=1
)
htmldb.to_html("table.html", show_dimensions=True, na_rep="")

# Finally let's output planes.csv which is just the ICAO
planesdb = htmldb.drop(["$Registration", "$Operator", "$Type", "$ICAO Type"], axis=1)
# add an empty column so we have a , separator
planesdb["Blank"] = ""
planesdb.to_csv("planes.csv")
