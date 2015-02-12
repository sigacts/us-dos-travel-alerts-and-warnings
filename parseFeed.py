#!/usr/bin/env python

import urllib2
import sqlite3
from lxml import etree
from pykml import parser
from xml.dom.minidom import parseString
from pykml.factory import KML_ElementMaker as KML

import os
filePath = os.path.dirname(os.path.abspath(__file__))
fileName = 'countriesFIPs.sqlite'


def dbExecution(sqlCmd, sqlData):
	try:
		con = sqlite3.connect(filePath + '/' + fileName)
		cur = con.cursor()
		cur.execute(sqlCmd, (sqlData))
		resultList = cur.fetchall()
		con.commit()
		cur.close()
		con.close()
	except sqlite3.Error as e:
		resultList = 'An error occurred: ' + e.args[0]
		pass
	
	return resultList


def CreateKMLDoc():
	kmlobj = KML.kml()
	return kmlobj


def MakeKMLFolder():
	kmlfolder = KML.Folder()
	return kmlfolder


def AddPlacemark(lat, lon, itemTitle, itemDesc, feedDetails):
	myCoords = str(lon) + ',' + str(lat)
	popupContent = itemDesc
	kmlStyle = feedDetails['kmlStyle']

	placemark = KML.Placemark(
		KML.name(itemTitle),
		KML.styleUrl(kmlStyle),
		KML.Point(
			KML.coordinates(myCoords)
		),
		KML.description(popupContent)
	)
	
	return placemark


def DefinePlacemarkStyle(feedDetails):
	iconURL = feedDetails['iconURL']
	kmlStyle = feedDetails['kmlStyle']

	style = KML.Style(
        KML.IconStyle(
	    	KML.scale(1.6)
    	),
		KML.Icon(
			KML.href(iconURL),
		),
        KML.LabelStyle(
			KML.scale(0)
		),
		KML.BalloonStyle(
			KML.text("""<h2>$[name]</h2><br><br><text>$[description]</text>"""),
		),
		id = kmlStyle
	)
	return style


def getFile(feedDetails):
	requestURL = feedDetails['feedURL']
	pageRequest = urllib2.Request(requestURL)
	pageContent = urllib2.urlopen(pageRequest).read()

	return pageContent


def parseXML(dom):
	itemList = []
	for i in dom.getElementsByTagName('item'):
		itemTitle = i.getElementsByTagName('title')[0].firstChild.wholeText
		itemTitle = itemTitle.strip()
		itemDate = i.getElementsByTagName('pubDate')[0].firstChild.wholeText
		itemDate = itemDate.strip()
		itemLink = i.getElementsByTagName('link')[0].firstChild.wholeText
		itemLink = itemLink.strip()
		itemLoc = i.getElementsByTagName('dc:identifier')[0].firstChild.wholeText
		itemLoc = itemLoc.strip()
		itemDesc = i.getElementsByTagName('description')[0].firstChild.wholeText
		itemDesc = itemDesc.strip()

		itemEntry = [itemTitle, itemDate, itemLink, itemLoc, itemDesc]
		itemList.append(itemEntry)

	return itemList


def generateKML(itemList, feedDetails):
	kmlobj = CreateKMLDoc()

	kmlfolder = MakeKMLFolder()
	kmlobj.append(kmlfolder)

	folderName = feedDetails['folderName']

	kmlobj.Folder.append(KML.name(folderName))

	kmlstyle = DefinePlacemarkStyle(feedDetails)
	kmlobj.Folder.append(kmlstyle)

	for item in itemList:
		myTitle = item[0]
		myLoc = item[3]

		if len(myLoc) > 0:
			locateList = myLoc.split(',')
		else:
			locateList = ['World']

		for itemLocation in locateList:
			myDesc = item[4]

			sqlData = [itemLocation]
			sqlCmd = 'select countryLat, countryLon from countryTbl where countryCode = ?'
			resultList = dbExecution(sqlCmd, sqlData)

			try:
				myLat = resultList[0][0]
				myLon = resultList[0][1]
			except:
				myLat = 0
				myLon = 0

			if len(locateList) > 0:
				myPlacemark = AddPlacemark(myLat, myLon, myTitle, myDesc, feedDetails)
				kmlobj.Folder.append(myPlacemark)

	docContent = etree.tostring(etree.ElementTree(kmlobj), pretty_print=True)

	return docContent


def main():

	warningDetails = {	'folderName': 'U.S. DOS Travel Warnings',
						'kmlStyle': 'travelWarning',
						'feedURL': 'http://travel.state.gov/_res/rss/TWs.xml',
						'iconURL': 'http://travel.state.gov/etc/designs/passports/images/icon_warning_large.png'}

	alertDetails = {	'folderName': 'U.S. DOS Travel Alerts',
						 'kmlStyle': 'travelAlerts',
						 'feedURL': 'http://travel.state.gov/_res/rss/TAs.xml',
						 'iconURL': 'http://travel.state.gov/etc/designs/passports/images/icon_alert_large.png'}

	feedDetails = warningDetails

	data = getFile(feedDetails)
	dom = parseString(data)
	itemList = parseXML(dom)

	docContent = generateKML(itemList, feedDetails)
	print docContent


if __name__ == "__main__":
	main()