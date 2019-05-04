from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

print('Email: ')
email = input()
print('Matricola: ')
id = input()

# access statistica page
url = 'http://datascience.maths.unitn.it/ocpu/library/doexercises/www/'
driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)

# wait for the page to be loaded
wait = WebDriverWait(driver, 86400) # 1 day
wait.until(EC.visibility_of_element_located((By.ID, "email_address")))

# get email and matricola values from the page
print('Login: ' + email + ' - ' + id)
email = email.lower()
email = email.replace(" ","")
print('Mail:'+email)
driver.find_element_by_id('email_address').send_keys(email)
driver.find_element_by_id('matricola').send_keys(id)
driver.find_element_by_id('signin').click()

# wait after login page to be loaded
wait.until(EC.visibility_of_element_located((By.ID, "link_res")))
driver.find_element_by_id('date').send_keys('05/01/2019')
counter = 0
while(1):
  try:
    driver.find_element_by_id('tokenrequest').click()
  except:
    print('no click')
  try:
    driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[1]/button').click()
  except:
    print('box of wrong credentials not found ' + str(counter))
  counter += 1