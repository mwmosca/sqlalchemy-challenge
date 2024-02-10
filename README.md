# sqlalchemy-challenge
Module 10 Challenge Submission

## Context
You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area.

## Usage
Download the SurfsUp directory, **maintaining the file structure**.<br>
<br>
To explore the climate data analysis, run the climate.ipynb Jupyter notebook.<br>
<br>
To view the climate app, launch app.py and navigate to the active server on an internet browser. The landing page lists the available routes. Append them to the base url to navigate to the respective pages:<br>
<br>
/api/v1.0/precipitation - displays a JSON dictionary containing dates and precipitation data from the most recent year in the dataset<br>
/api/v1.0/stations - displays a JSON list of the 9 stations in the dataset<br>
/api/v1.0/tobs - displays a JSON dictionary containing dates and temperature data from the most active station during the most recent year in the dataset<br>
/api/v1.0/\<start\> - displays the minimum, average, and maximum values of the temperature data from the \<start\> date to the most recent date in the dataset<br>
/api/v1.0/\<start\>/\<end\> - displays the minimum, average, and maximum values of the temperature data from the \<start\> date to the \<end\> date<br>
<br>
Dates must be entered in one of the following formats:<br>
yyyy-m-d<br>
yyyy-mm-d<br>
yyyy-m-dd<br>
yyyy-mm-dd
