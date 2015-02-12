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

To choose alerts or warnings, alter the `feedDetails` variable in the `main` function to either the `warningDetails` or the `alertDetails` dictionaries.

### Travel Warnings Location
`http://travel.state.gov/_res/rss/TWs.xml`

### Travel Alerts Locations
`http://travel.state.gov/_res/rss/TAs.xml`

### Sample KML in Google Earth
![](http://www.sigacts.com/images/US-DOS-Travel-Notifications-To-KML.png)
