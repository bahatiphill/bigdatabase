"""
Author: Igwaneza Bruce <knowbeeinc@gmail.com>
Attempting to collect useful data from google maps
Source: google maps
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from rwavalidator import isPhoneNumber
from tqdm import tqdm
import time
import json
import os
import glob
import threading



locations = [
'Bugesera',
'Gatsibo',
'Kayonza',
'Kirehe',
'Ngoma',
'Nyagatare',
'Rwamagana',
'Gasabo',
'Kicukiro',
'Nyarugenge',
'Burera',
'Gakenke',
'Gicumbi',
'Musanze',
'Rulindo',
'Gisagara',
'Huye',
'Kamonyi',
'Muhanga',
'Nyamagabe',
'Nyanza',
'Nyaruguru',
'Ruhango',
'Karongi',
'Ngororero',
'Nyabihu',
'Nyamasheke',
'Rubavu',
'Rusizi',
'Rutsiro']


def app():
    prompt = str(input("What are you looking for?: "))
    formatted_prompt = prompt.replace(" ", "+")
    
    for location in locations:
        query = f"{formatted_prompt}+in+{location}"
        getByLocation(query, location, prompt)
    
    browser = get_browser()    
    # after fetching everything, merge them into a single file
    for f in glob.glob(f"{country}/{prompt}/*.json"):
        with open(f, "r") as file:
            try:
                for d in json.load(file):
                    results.append(d)
            except ValueError:
                print(f)
    with open(f"{country}/{prompt}.json", "w") as output:
        json.dump(results, output)
    print("done")
    browser.quit()



results = []
country = 'Rwanda'   
threadLocal = threading.local()

def get_browser():
  browser = getattr(threadLocal, 'browser', None)
  if browser is None:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-notifications")
    options.add_argument("--log-level=3"); 
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    browser = webdriver.Chrome(options=options, service_log_path=None)
    browser.delete_all_cookies()
    setattr(threadLocal, 'browser', browser)
  return browser
 
def getTitle(t):
    return t.split('\n')[0].strip()

def getPhone(text):
    phone = text.split('⋅')[-1].split('·')[-1].replace(" ", "")
    if isPhoneNumber(phone):
        return phone
    else:
        return 'No phone number'


def getByLocation(query, location, prompt):
    browser = get_browser()
    url = f"https://www.google.com/search?sxsrf=ACYBGNTuYn04lHdVfa6QBkoHVHDxaEfr0Q:1578597416649&q={query}&npsic=0&rflfq=1&rlha=0&tbm=lcl&ved=2ahUKEwjT1IzSnffmAhXn1uAKHaimC3EQjGp6BAgLEDQ&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2&rldoc=1#rlfi=hd:;tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2"
    browser.get(url)
    data=[]
    while True:
        try:
            # get all cards containing data we need
            cards = browser.find_elements_by_class_name("cXedhc")
           
            for title in tqdm(cards,desc=f"scraping for {location}"):
                data.append({'name':getTitle(title.text),'location':location, 'tel':getPhone(title.text)})
            # print a new line for a nice progress bar
            print("\n")
            browser.find_element_by_xpath("//*[@id='pnnext']").click() # find and click on the next button element
            if(EC.invisibility_of_element((By.XPATH, "//*[@id='rl_ist0']/div[1]/div[2]/div"))): #check to see if the page is still loading, with a little spinner
                time.sleep(1)
        except (TimeoutException, WebDriverException) as e:
            if not os.path.exists(f'{country}/{prompt}'):
                os.makedirs(f'{country}/{prompt}')
            with open(f'{country}/{prompt}/{location}.json', 'w') as file:
                json.dump(data, file)
            print(f'found {len(data)} {prompt} from {location}')
            break
