#Automatic Survey Completer for UCSC Daily COVID Student Survey
#Created by Tim Kraemer
#Created on February 9th, 2022

#import libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import smtplib
from datetime import date
from email.message import EmailMessage
import imghdr

#initialize login info
ucsc_username = "tikraeme"
ucsc_password = "ticktricktrack13"
gmail_email = "ucsc.covid.emails@gmail.com"
gmail_password = "ticktricktrack13"
ID = "id"
XPATH = "xpath"
NAME = "name"

#initialize the Google Chrome Driver
driver = webdriver.Chrome("chromedriver")

#open UCSC health website
driver.get("https://studenthealth.ucsc.edu")

#freeze program for 10 seconds
time.sleep(0.5)

#find login and input username
driver.find_element(By.ID, "username").send_keys(ucsc_username)
time.sleep(0.5)

#input password
driver.find_element(By.ID, "password").send_keys(ucsc_password)
time.sleep(0.5)

#click on login
driver.find_element(By.NAME, "_eventId_proceed").click()
time.sleep(0.5)

#Push send push notification button
driver.switch_to.frame("duo_iframe")
driver.find_element(By.XPATH, "//*[@id='auth_methods']/fieldset/div[1]/button").click()
time.sleep(10)

#input date of birth
#select month
select = Select(driver.find_element(By.ID, "dtDOBMN"))
select.select_by_visible_text("Feb")
#select day
select = Select(driver.find_element(By.ID, "dtDOBDY"))
select.select_by_visible_text("24")
#type in year
year_element = driver.find_element(By.ID, "dtDOBYR")
year_element.send_keys("2002")
#click on submit
driver.find_element(By.ID, "cmdStandardProceed").click()

#click on complete survey
driver.find_element(By.XPATH, "//*[@id='ctl03']/div[3]/div/a").click()

#click on continue
driver.find_element(By.XPATH, "//*[@id='mainbody']/div[2]/div[1]/div/div[2]/a").click()

#answer questions
driver.find_element(By.XPATH, "//*[@id='mainbody']/main/form/div[2]/fieldset/div[2]").click()
driver.find_element(By.XPATH, "//*[@id='mainbody']/main/form/div[3]/fieldset/div/div[2]/div").click()
driver.find_element(By.XPATH, "//*[@id='mainbody']/main/form/div[4]/fieldset/div/div[2]/div").click()
driver.find_element(By.XPATH, "//*[@id='mainbody']/main/form/div[5]/fieldset/div/div[2]/div").click()
driver.find_element(By.XPATH, "//*[@id='mainbody']/main/form/div[6]/fieldset/div/div[2]/div").click()
driver.find_element(By.XPATH, "//*[@id='mainbody']/main/form/div[7]/fieldset/div[1]").click()

#click continue
driver.find_element(By.XPATH, "//*[@id='mainbody']/footer/div/div[2]/input").click()

#show quarantine badge
driver.find_element(By.ID, "showQuarantineBadge").click()
time.sleep(2)

#take screenshot
driver.save_screenshot("CovidSurvey.png")

#close the driver
driver.close()

#send an email
date = date.today()
date_time_stamp = date.strftime("%d/%m/%Y")
subject = 'UCSC Covid Survey Result ' + date_time_stamp
msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = gmail_email
msg['To'] = 'tikraeme@ucsc.edu'

with open('CovidSurvey.png', 'rb') as f:
    file_data = f.read()
    file_type = imghdr.what(f.name)
    file_name = f.name

msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(gmail_email, gmail_password)
    smtp.send_message(msg)


