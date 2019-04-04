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
sheet = gc.open("Voti statistica").get_worksheet(2)

# access statistica page
url = 'http://datascience.maths.unitn.it/ocpu/library/doexercises/www/'
driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

wait = WebDriverWait(driver, 20)

for student in range(1,500):
  try:
    # wait for the page to be loaded
    wait.until(EC.visibility_of_element_located((By.ID, "email_address")))

    # get email and matricola values from the page
    matricola = sheet.cell(student,1).value
    cognome = sheet.cell(student,2).value
    nome = sheet.cell(student,3).value

    print('Login: ' + nome + ' ' + cognome + ' ' + matricola)

    email = nome.lower()+'.'+cognome.lower()
    email = email.replace(" ","")

    # write values in the page
    driver.find_element_by_id('email_address').send_keys(email)
    driver.find_element_by_id('matricola').send_keys(matricola)
    driver.find_element_by_id('signin').click()

    try:
      wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="formindex"]/div[1]/div')))
      sheet.cell(student,4).value='not found'
      print('not found')
    except:
      sheet.cell(student,4).value = "found"
      print('found')

# NOT WORKING WHEN I TRY TO WRITE A VALUE IN SPREADSHEET

    driver.refresh()
  except:
    print('Done')
    break
driver.close()