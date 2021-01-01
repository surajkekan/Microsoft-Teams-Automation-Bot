from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import os.path
from os import path
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException        

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")

opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })

driver = None
URL = "https://teams.microsoft.com"

CREDS = {'email' : 'example@gmail.com','passwd':'password'}
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def convert24(str1): 
    if(len(str1)==7):
        str1='0'+str1
    if str1[-2:] == "AM" and str1[:2] == "12": 
        return "00" + str1[2:-2]      
    elif str1[-2:] == "AM": 
        return str1[:-2]
    elif str1[-2:] == "PM" and str1[:2] == "12": 
        return str1[:-2] 
    else: 
        return str(int(str1[:2]) + 12) + str1[2:6] 
def get_end_time(text):
    a=text.split(",")
    temp=a[-2].split()
    f2=temp[8]
    end_time=temp[2]+' '+f2
    return convert24(end_time)

def meet_runtime(end_time):
    datetime.now().minute
    t1=((int(end_time.split(":")[0])*60)+(int(end_time.split(":")[1])))*60
    t2=(datetime.now().hour*60+datetime.now().minute)*60
    return t2-t1
def join_meeting():
	while True:
		if check_exists_by_xpath('//*[@aria-label="Join meeting"]'):
			driver.find_element_by_xpath('//*[@aria-label="Join meeting"]').click()
			time.sleep(5)
			if check_exists_by_xpath('//*[@telemetry-summary="Toggle camera OFF in meeting pre join screen"]'):
				driver.find_element_by_xpath('//*[@telemetry-summary="Toggle camera OFF in meeting pre join screen"]').click()
				print("Turned Off Camera")
				time.sleep(2)
			if check_exists_by_xpath('//toggle-button[@telemetry-summary="Toggle microphone OFF in meeting pre join screen"]'):
				driver.find_element_by_xpath('//toggle-button[@telemetry-summary="Toggle microphone OFF in meeting pre join screen"]').click()
				print("Turned off Microphone")
				time.sleep(2)
			driver.find_element_by_xpath('//*[@aria-label="Join the meeting"]').click()
			print("Currently In Meeting")
			time.sleep(5)
			driver.find_element_by_xpath('//*[@id="app-bar-ef56c0de-36fc-4ef8-b417-3d82ba9d073c"]').click()
			time.sleep(5)
			on_going_meeting=driver.find_element_by_xpath('//*[@class="node_modules--msteams-bridges-components-calendar-event-card-dist-es-src-renderers-event-card-renderer-event-card-renderer__eventCard--h5y4X node_modules--msteams-bridges-components-calendar-event-card-dist-es-src-renderers-event-card-renderer-event-card-renderer__activeCall--25Ch-"]')
			att=on_going_meeting.get_attribute('aria-label')
			end_time=get_end_time(att)
			runtime=meet_runtime(end_time)
			if(runtime<=0):
				driver.find_element_by_xpath('//*[@id="hangup-button"]').click()
			else:
				time.sleep(runtime)
				driver.find_element_by_xpath('//*[@id="hangup-button"]').click()
				time.sleep(5)
			driver.refresh()
		else:
			driver.refresh()
			time.sleep(30)
