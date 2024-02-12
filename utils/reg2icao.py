#!/usr/bin/env python

import pandas as pd

infile = pd.read_csv("in.csv", header=0)

# aircraft list uses a ; instead of a comma
aircraftlist = pd.read_csv(
    "aircraft.csv",
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
    ],
)

# print(infile)
# print(aircraftlist)


Left_join = pd.merge(infile, aircraftlist, on="$Registration", how="left")

Left_join.to_csv("out.csv")
