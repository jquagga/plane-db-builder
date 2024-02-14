#!/usr/bin/env python

import pandas as pd

infile = pd.read_csv(
    "in.csv",
).set_index("$Registration")

# print(infile)

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
).set_index("$Registration")

# print(infile)
# print(aircraftlist)

# infile.update(aircraftlist)

# print(infile)
Left_join = pd.merge(infile, aircraftlist, on="$Registration", how="left")

Left_join.to_csv("out.csv")
