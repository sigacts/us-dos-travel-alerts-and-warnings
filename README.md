# Convert US Department of State Travel Alerts and Warnings to KML

This utility parses travel alerts and travel warnings from the U.S. Department of State and outputs a KML file for geospatial visualization.

The alerts and warnings are formatted as XML.

### Documentation
Run `parseFeed.py` from the command line to output KML.

The sample KML files were generated from the terminal window using these commands:
```
python parseFeed.py > Sample-Travel-Warnings-2015-02-12.kml
```
```
python parseFeed.py > Sample-Travel-Alerts-2015-02-12.kml
```

To choose whether to parse alerts or warnings, alter the `feedDetails` variable in the `main` function to either the `warningDetails` or the `alertDetails` dictionaries.

#### Country 
The Department of State KML feeds reference countries with a two digit FIPS identifier provided in the `<dc:identifier>` XML tag.

A collection of identified FIPS codes are stored in the `countryTbl` table of the `countriesFIPs.sqlite` SQLite database. Each FIPS code is stored as a unique 'countryCode' value with corresponding `countryName`, `countryLat`, and `countryLon` values. The latitude and longitude of each country plot to the centroid of the nation's boundaries.

#### Handling Location Exceptions
If an alert or a warning has multiple countries listed, a unique placemark is created for each country.

If there is no location listed for an alert or a warning, the placemark is set to a `World` location and plotted at the coordinates 0, 0 (latitude and longitude).

#### Travel Warnings Location
`http://travel.state.gov/_res/rss/TWs.xml`

#### Travel Alerts Locations
`http://travel.state.gov/_res/rss/TAs.xml`

#### Sample KML in Google Earth
![](http://www.sigacts.com/images/US-DOS-Travel-Notifications-To-KML.png)
