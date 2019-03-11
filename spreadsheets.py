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

# get email and matricola values from the page
email = sheet.cell(2,1).value
matricola = sheet.cell(2,2).value
print(email + ' ' + matricola)

# access statistica page
url = 'http://datascience.maths.unitn.it/ocpu/library/doexercises/www/'
driver = webdriver.Chrome(r"D:\Users\Marco\Downloads\chromedriver.exe")
driver.get(url)

# wait for the page to be loaded
wait = WebDriverWait(driver, 15)
wait.until(EC.visibility_of_element_located((By.ID, "email_address")))

# write values in the page
driver.find_element_by_id('email_address').send_keys(email)
driver.find_element_by_id('matricola').send_keys(matricola)
driver.find_element_by_id('signin').click()

# click for table with marks
wait.until(EC.visibility_of_element_located((By.ID, "link_res")))
driver.find_element_by_id('link_res').click()

# count rows and cols
wait.until(EC.visibility_of_element_located((By.ID, "results_table")))
rowCount = len(re.findall("<tr>",driver.page_source))-1 # -1 to remove thead

for x in range(rowCount):
  print(x+1)
  datePath = '//*[@id="results_table"]/tbody/tr['+str(x)+']/td[2]'
  markPath = '//*[@id="results_table"]/tbody/tr['+str(x)+']/td[3]'
  selectedDate = driver.find_element_by_xpath(datePath).text
  selectedMark = driver.find_element_by_xpath(markPath).text
  print(selectedDate + ' - ' + selectedMark)
# for size table, get date and mark (this page)
# insert them into spreadsheet (sheets.py)

driver.close()