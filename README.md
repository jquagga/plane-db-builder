# plane-db-builder

plane-db-builder is the small python companion to [upa](https://github.com/jquagga/upa) [docker-planefence](https://github.com/sdr-enthusiasts/docker-planefence) written by Ramon F. Kolb. It builds a custom list of aircraft ADSB transponder codes from the large standard list to use on your local ADSB receiver to send out notifications for those planes.

## Installation

This script requires python and pandas. Also you need to download aircraft.csv.gz from the tar1090 distribution and plane-alert-db.csv from the sdrenthusists repository. Together the script will search and populate a plane-alert-db-custom.csv for planealert and a planes.csv for upa.

## Configuration

Changing the filtering paramaters used in this section of the script lets you pick out different categories or tags to "cherry pick" from the master sheet.

```python
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
```

## Contributing

Pull requests are welcome! However since this is largely a "customize the rules my way" type of deal, you probably want to fork this repo and change the rules section of plane-db-builder.py to pick out the planes you may want to track. Maybe you only want the KC-130s that I pulled out or don't want to be notified when a P51 flys by. Edit away!
