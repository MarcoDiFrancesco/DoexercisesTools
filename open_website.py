from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import time
username = 'marco.difrancesco'
matricola = '202351'

url = 'http://datascience.maths.unitn.it/ocpu/library/doexercises/www/'
driver = webdriver.Chrome(r"D:\Users\Marco\Downloads\chromedriver.exe")
driver.get(url)

wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.ID, "email_address")))

driver.find_element_by_id('email_address').send_keys(username)
driver.find_element_by_id('matricola').send_keys(matricola)
driver.find_element_by_id('signin').click()

wait.until(EC.visibility_of_element_located((By.ID, "link_res")))
driver.find_element_by_id('link_res').click()

