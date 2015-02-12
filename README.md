# Convert US Department of State Travel Alerts and Warnings to KML

This utility parses travel alerts and travel warnings from the U.S. Department of State and outputs a KML file for geospatial visualization.

The native format of the alerts and warnings is XML.

### Documentation
Run `python parseFeed.py` from the command line to output KML.

The sample KML files were generated from the terminal window using these commands:
```
python parseFeed.py > Sample-Travel-Warnings-2015-02-12.kml
```
```
python parseFeed.py > Sample-Travel-Alerts-2015-02-12.kml
```

To choose whether the script parses alerts or warnings, set the `feedDetails` variable in the `main` function of `parseFeed.py` to reference either the `warningDetails` or the `alertDetails` dictionaries.

#### Country Locations
The Department of State XML feeds reference countries with a two digit FIPS identifier provided in the `<dc:identifier>` XML tag.

A collection of identified FIPS codes are available in the `countriesFIPs.sqlite` SQLite database.

Each FIPS code is stored in the `countryTbl` table as a unique `countryCode` row with corresponding `countryName`, `countryLat`, and `countryLon` values.

The latitude (`countryLat`) and longitude (`countryLon`) of each country plot to the centroid of that nation's boundaries.

#### Handling Location Exceptions
If an alert or a warning has multiple countries listed, a unique placemark is created at the centroid of each referenced country.

If there is no location listed for an alert or a warning, the placemark is set to a `World` location and plotted at the coordinates 0, 0 (latitude and longitude).

#### Travel Warnings Feed
`http://travel.state.gov/_res/rss/TWs.xml`

#### Travel Alerts Feed
`http://travel.state.gov/_res/rss/TAs.xml`

#### Sample KML in Google Earth
![](http://www.sigacts.com/images/US-DOS-Travel-Notifications-To-KML.png)
