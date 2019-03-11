import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# login to spreadsheet
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
gc = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name('credentials.json',scope))
sheet = gc.open("Voti statistica").sheet1

testDate = '2019-03-08'
selectedMark = 20
# search for the postition of the date
# example output: <Cell R1C7 '2019-03-08'>
cellDatePosition = str(sheet.findall(testDate))

# take first number after R and C, (it is in an array beacuse of re)
row = int(re.findall(r'R(\d+)',cellDatePosition)[0])
col = int(re.findall(r'C(\d+)',cellDatePosition)[0])

print('row:', row, 'col:', col)
sheet.update_cell(row+1,col,selectedMark)