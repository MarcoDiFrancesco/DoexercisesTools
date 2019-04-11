import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# login to spreadsheet
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
gc = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope))
sheet = gc.open("Voti statistica").get_worksheet(2)

# access statistica page
url = 'http://datascience.maths.unitn.it/ocpu/library/doexercises/www/'
driver = webdriver.Chrome("chromedriver.exe")
driver.set_window_size(800, 600)
driver.get(url)

# load webdriver
wait = WebDriverWait(driver, 20)

# check column number for Matricola, Nome, Cognome, Stato
cellPosition = str(sheet.findall('ID'))
colId = int(re.findall(r'C(\d+)', cellPosition)[0])
cellPosition = str(sheet.findall('Surname'))
colSurname = int(re.findall(r'C(\d+)', cellPosition)[0])
cellPosition = str(sheet.findall("Name"))
colName = int(re.findall(r'C(\d+)', cellPosition)[0])

# get number of users inside the spreadsheet
arrayId = sheet.col_values(colId)
arraySurname = sheet.col_values(colSurname)
arrayName = sheet.col_values(colName)
arrayDate = sheet.row_values(1)

# remove the first 4 values: ID, Surname, Name, Media
arrayDate.pop(0)
arrayDate.pop(0)
arrayDate.pop(0)
arrayDate.pop(0)

# shift array of one to make it in line with spreadsheet columns
arrayId.insert(0, '')
arraySurname.insert(0, '')
arrayName.insert(0, '')

for student in range(2, len(arraySurname)):
	# wait for the page to be loaded
	wait = WebDriverWait(driver, 20)
	wait.until(EC.visibility_of_element_located((By.ID, "email_address")))

  # get email and matricola values from the page
	id = arrayId[student]
	surname = arraySurname[student]
	name = arrayName[student]

	email = name.lower()+'.'+surname.lower()
	email = email.replace(" ", "")

	print('Login: ' + email + ' ' + id)

	if id == ' ' or surname == ' ' or name == ' ':
		print('skip')
	else:
		# write values in the page
		driver.find_element_by_id('email_address').clear()
		driver.find_element_by_id('matricola').clear()

		driver.find_element_by_id('email_address').send_keys(email)
		driver.find_element_by_id('matricola').send_keys(id)
		driver.find_element_by_id('signin').click()

		# click for table with marks
		wait.until(EC.visibility_of_element_located((By.ID, "link_res")))
		driver.find_element_by_id('link_res').click()

		# count rows and cols
		wait.until(EC.visibility_of_element_located((By.ID, "results_table")))
		rowCount = len(re.findall("<tr>", driver.page_source)) - 1  # -1 to remove thead

		# if user has no marks
		if rowCount == 0 or rowCount == 1:
			print('no marks found')
		else:
			# there will be more or less 60 marks
			date = [0] * 100
			mark = [0] * 100

			for x in range(1, rowCount+1):
				datePath = '//*[@id="results_table"]/tbody/tr['+str(x)+']/td[2]'
				markPath = '//*[@id="results_table"]/tbody/tr['+str(x)+']/td[3]'
				selectedDate = driver.find_element_by_xpath(datePath).text
				selectedMark = driver.find_element_by_xpath(markPath).text
				date[x] = selectedDate
				mark[x] = selectedMark
				print(str(selectedMark)+' - '+str(selectedDate))

			# update mark from selected data
			arrayStudent = sheet.range('E'+str(student)+':CA'+str(student))

			for x in range(0, rowCount+1):
				selectedDate = date[x]
				selectedMark = mark[x]
				# check if the date was used in the page
				if selectedDate != 0:
					positionDate = arrayDate.index(selectedDate)
					arrayStudent[positionDate].value = float(selectedMark)

			sheet.update_cells(arrayStudent)
		driver.refresh()
driver.close()