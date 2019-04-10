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
sheet = gc.open("Voti statistica").get_worksheet(1)

# access statistica page
url = 'http://datascience.maths.unitn.it/ocpu/library/doexercises/www/'
driver = webdriver.Chrome("chromedriver.exe")
driver.set_window_size(800,600)
driver.get(url)

# load webdriver
wait = WebDriverWait(driver, 20)

# check column number for Matricola, Nome, Cognome, Stato
cellPosition = str(sheet.findall('ID'))
colId = int(re.findall(r'C(\d+)',cellPosition)[0])
cellPosition = str(sheet.findall('Surname'))
colSurname = int(re.findall(r'C(\d+)',cellPosition)[0])
cellPosition = str(sheet.findall("Name"))
colName = int(re.findall(r'C(\d+)',cellPosition)[0])
cellPosition = str(sheet.findall("Status"))
colStatus = int(re.findall(r'C(\d+)',cellPosition)[0])

# get number of users inside the spreadsheet
arrayId = sheet.col_values(colId)
arraySurname = sheet.col_values(colSurname)
arrayName = sheet.col_values(colName)
arrayStatus = sheet.col_values(colStatus)
# shift array of one to make it in line with spreadsheet columns
arrayId.insert(0,'')
arraySurname.insert(0,'')
arrayName.insert(0,'')
arrayStatus.insert(0,'')

for student in range(2,len(arraySurname)):
  # wait for the page to be loaded
  wait.until(EC.visibility_of_element_located((By.ID, "email_address")))

  # get email and matricola values from the page
  id = arrayId[student]
  surname = arraySurname[student]
  name = arrayName[student]
  # try to get status, if throws array out of bound make it empty
  try:
    status = arrayStatus[student]
  except:
    status = ''

  # create email from name and surname
  email = name.lower()+'.'+surname.lower()
  email = email.replace(" ", "")

  print(
    'Login: ' + id + ' - '
    + surname + ' '
    + name + ' - '
    + email + ' '
    + status
  )

  # if status is set to ok, skip it
  if status == 'ok' or status == 'no' :
    print("Already checked")
  elif id == '' or surname == '' or name == '':
    print("Missing value")
  else:
    # write values in the page
    driver.find_element_by_id('email_address').send_keys(email)
    driver.find_element_by_id('matricola').send_keys(id)
    driver.find_element_by_id('signin').click()

    try:
      wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div[1]/button')))
      # remove alert box of not found
      driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/button').click()
        # wait until error box disappears
      wait.until_not(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div[1]/button')))
      # clear email and matricola boxes
      driver.find_element_by_id('email_address').clear()
      found = 0
    except:
      # if found
      found = 1
      driver.refresh()

    if found == 0:
      try:
        # try with 'email-1' and wait again
        email = name.lower()+'.'+surname.lower()+'-1'
        email = email.replace(" ","")
        driver.find_element_by_id('email_address').send_keys(email)
        driver.find_element_by_id('signin').click()
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div[1]/button')))
        # remove alert box of not found
        driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/button').click()
        # wait until error box disappears
        wait.until_not(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div[1]/button')))
        # clear email and matricola boxes
        driver.find_element_by_id('email_address').clear()
        found = 0
      except:
        # if found
        found = 2
        driver.refresh()
      if found == 0:
        try:
          # try with 'email-2' and wait again
          email = name.lower()+'.'+surname.lower()+'-2'
          email = email.replace(" ","")
          driver.find_element_by_id('email_address').send_keys(email)
          driver.find_element_by_id('signin').click()
          wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div[1]/button')))
          # remove alert box of not found
          driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/button').click()
          # wait until error box disappears
          wait.until_not(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div[1]/button')))
          # clear email and matricola boxes
          driver.find_element_by_id('email_address').clear()
          driver.find_element_by_id('matricola').clear()
          found = 0
        except:
          # if found
          found = 3
          driver.refresh()
    if found == 0:
      print("not found")
      sheet.update_cell(student,colStatus,'no')
    elif found == 1:
      print("found in " + email)
      sheet.update_cell(student,colStatus,'ok')
    elif found == 2:
      print("found in " + email)
      sheet.update_cell(student,colStatus,'ok')
      sheet.update_cell(student,colSurname,surname+"-1")
    elif found == 3:
      print("found in " + email)
      sheet.update_cell(student,colStatus,'ok')
      sheet.update_cell(student,colSurname,surname+"-2")
driver.close()