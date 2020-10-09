# SportsTracker_activity_export
This repository hosts a small project related to activity export from Sports Tracker (sports-tracker.com). At the moment, there is no way to mass export activities from Sports Tracker provided by the company and this small script solves the issue. The script exports all Sports Tracker acitivities to **.gpx** files, compatible with Strava, Garmin and other services.

### Repository content
--------
*  main.py file - Program init
*  sports_tracker_api.py file - Containing some site interaction functions

### Requirements
--------
*  A valid Sports Tracker account
*  Python 3 installed
*  Python packages installed (requests, json, xml.etree)

The script is pretty simple and currently supporting (walking, running, cycling, hiking, other) activity types.
In order to use the program, an **authentication token** is needed that must be acquired while logged in to sports-tracker.com.

### How to run
--------
From the command line run: <br/>
*python spt_export.py -t <your authentication token> -o <output file directory>*
