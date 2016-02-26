Hydro-Québec power outages notifier
===========
This project queries Hydro-Québec website for changes in power outages statuses for a specific location. By giving one part of the two dimensions GPS coordinates of the desired location, the informations on the power outage at this location will be returned. Such informations are: 
- number of clients affected
- beginning and estimed end times of outage
- cause
- status of repair

This information is available on Hydro-Québec website on a interactive map with graphicals polygons representing power outages. Such data representations is great for humans but not for scripts that extracts the data to detect changes in statuses. This script is using their undocumented API that is used by their iOS mobile app.

With its design, the script is easily used as a modification checker. By calling it multiple times, you can monitor change and do your favorite notification action by implemented the "notify()" function.

Usage
=========
The Python script has one required argument: the dimension of the GPS coordonates (either "lat" or "long", respectively for "latitude" and "longitude" appended with the value of the coordinate. These elements should be joined by a colon.

> python3 hydro.py lat:45.5054

> python3 hydro.py long:-73.615




It is recommended to give 3 or 4 digits after the decimal point because the informations returned can only be about one power outage. With less precise coordinates, more than one power outage zone with be targeted and the execution will stop.


Development process
===========
Biggest part of the development was to understand the undocumented API used by the interactive map to gather its data. With the Web proxy Burp Suite, I was able to inspect every part of the HTTP traffic to understand the values of most of the fields and get the addresses to request the informations.


Dependencies
=====
- Python 3
- Requests module

Motivation
==========
Like every other tool, one creates it only when it is needed. It had a use for this project when my home lost electricity due to freezing rain. On Hydro-Québec interactive map, it was listed that the power would come back 48 hours after the initial outage. I knew by experience that those estimate are unreliable so I needed a solution to monitor the informations on the interactive map.

TODO
=========
- Cache the status message dictionnary
- Uniformisation of language since this is very mixed with english and french
- Use of "logger" module
- Rename JSON variable since very few variables are actually JSON objects 
- Use of command-line argument module
- Orthograph in README

Attribution
=======
A big part of the exploratory work on the Hydro-Québec website was done by reddit user /u/notian which I found on the following thread: <https://www.reddit.com/r/montreal/comments/3ucyjo/developers_does_hydroquebec_have_an_api/>
