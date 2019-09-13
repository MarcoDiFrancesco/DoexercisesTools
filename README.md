# Doexercises Tools
## What's this?
This program is made to plot data of all the students that are attending Probability and Statistics class using [doexercises platform](http://datascience.maths.unitn.it/doexercises/).

With this programs you are able to:
* [Brute force ID numbers](https://github.com/MarcoDiFrancesco/DoexercisesTools/blob/master/bruteForceMatricola.py) (matricole) of students
* [Download marks](https://github.com/MarcoDiFrancesco/DoexercisesTools/blob/master/getMarks.py) of the students you have the ID number, and put them in a [Google Spreadsheet](https://docs.google.com/spreadsheets/)
* [Request token](https://github.com/MarcoDiFrancesco/DoexercisesTools/blob/master/requestToken.py) continuously (useful for the 1st May exercise)


## Plot example
[Spreadsheet of 2019 marks](https://docs.google.com/spreadsheets/d/1xDTFy_oSF6smH6gWwwt4T3QZtLoTRGazkQRKLxoxvhQ/pubhtml)  
*The students ID are not publicly available in the spreadsheet*

[![Spreadsheet screenshot](https://i.imgur.com/15HZLfp.png)](https://docs.google.com/spreadsheets/d/1xDTFy_oSF6smH6gWwwt4T3QZtLoTRGazkQRKLxoxvhQ/pubhtml)
## How to use it
Requirements:
* Python installed
* The gspread (Google Spreadsheets) libraries installed:  
`pip install gspread`
* Selenium libraries installed  
`pip install -U selenium`
* Oauth2client  
`pip install oauth2client`
* [Download](https://sites.google.com/a/chromium.org/chromedriver/downloads) selenium driver to make it working with Chrome, old version of the drivers is already present in the repository

The script [Download marks](https://github.com/MarcoDiFrancesco/DoexercisesTools/blob/master/getMarks.py) needs:
* A [Google Spreadsheet](https://docs.google.com/spreadsheets), once done copy the link key into the programs you want to use in the section  
`sheet = gc.open_by_key()`  
e.g. with the link  
```
https://docs.google.com/spreadsheets/d/1xDTFy_oSF6smH6gWwwt4T3QZtLoTRGazkQRKLxoxvhQ
```
write the last part of the link
```python
sheet = gc.open_by_key('1xDTFy_oSF6smH6gWwwt4T3QZtLoTRGazkQRKLxoxvhQ')
```

* Drive API on [Cloud console](https://console.developers.google.com/apis) to connect it with Spreadsheet, ([tutorial](https://developers.google.com/sheets/api/quickstart/python)), once downloaded the Spreadsheets API in JSON format, rename the file to `credentials.json` and put it the project folder

The output should look like:

<!-- cmd output downlaod marks -->
<img src="https://i.imgur.com/xi8IV3I.png" width="500">

Done 😊
