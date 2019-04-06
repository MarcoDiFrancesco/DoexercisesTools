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

arrayStatus = []
print(arrayStatus)
arrayStatus = [300]
print(arrayStatus)

# get number of users inside the spreadsheet
arrayId = sheet.col_values(colId)
arraySurname = sheet.col_values(colSurname)
arrayName = sheet.col_values(colName)
arrayStatus = sheet.col_values(colStatus)
print(arrayStatus)
for student in range(1,len(arraySurname)):
  # wait for the page to be loaded
  wait.until(EC.visibility_of_element_located((By.ID, "email_address")))

  # get email and matricola values from the page
  id = arrayId[student]
  surname = arraySurname[student]
  name = arrayName[student]
  try:
    status = arrayStatus[student]
  except:
    print()
    #NEED TO REMOVE THIS TRY CATCH
    # IT GOES OUT OF BOUND WHEN THERE ARE NO OK ANYMORE

  # create email from name and surname
  email = name.lower()+'.'+surname.lower()
  email = email.replace(" ","")

  print(
    'Login: ' + id + ' - '
    + surname + ' '
    + name + ' - '
    + email + ' '
    + status
  )

  # if status is set to ok, skip it
  if status == 'ok':
    print("Already checked")
  else:
    # write values in the page
    driver.find_element_by_id('email_address').send_keys(email)
    driver.find_element_by_id('matricola').send_keys(id)
    driver.find_element_by_id('signin').click()

    try:
      wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div[1]/button')))
      sheet.cell(student,colStatus).value = 'no'
      print('not found')
      # remove alert box of not found
      driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/button').click()
      # clear email and matricola boxes
      driver.find_element_by_id('email_address').clear()
      driver.find_element_by_id('matricola').clear()
    except:
      sheet.cell(student,colStatus).value = 'ok'
      print('found')
      driver.refresh()
driver.close()