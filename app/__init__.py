"""
Author: Igwaneza Bruce <knowbeeinc@gmail.com>
Attempting to collect useful data from google maps
Source: google maps
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from rwavalidator import isPhoneNumber
from tqdm import tqdm
import time
import json
import os
import glob

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
# def getLocation(t):
#     l = t.split('\n')[-2]
#     if l in ls:
#         return l
#     else:
#         return 'No address'

results = []    
def getTitle(t):
    return t.split('\n')[0].strip()

def getPhone(text):
    phone = text.split('⋅')[-1].split('·')[-1].replace(" ", "")
    if isPhoneNumber(phone):
        return phone
    else:
        return 'No phone number'


def app():
    prompt = str(input("What are you looking for?: "))
    formatted_prompt = prompt.replace(" ", "+")
    for location in locations:
        query = f"{formatted_prompt}+in+{location}"
        getByLocation(query, location, prompt)
        
    # after fetching everything, merge them into a single file
    for f in glob.glob(f"{prompt}/*.json"):
        with open(f, "r") as file:
            try:
                for d in json.load(file):
                    results.append(d)
            except ValueError:
                print(f)
    with open(f"{prompt}.json", "w") as output:
        json.dump(results, output)
    print("done")
    
def getByLocation(query, location, prompt):
    options = webdriver.ChromeOptions()

    options.add_argument("--headless")
    options.add_argument("--disable-notifications")
    options.add_argument("--log-level=3"); 
    
    browser = webdriver.Chrome(options=options, service_log_path=None)
    
    browser.delete_all_cookies()
    data=[]

    url = f"https://www.google.com/search?sxsrf=ACYBGNTuYn04lHdVfa6QBkoHVHDxaEfr0Q:1578597416649&q={query}&npsic=0&rflfq=1&rlha=0&tbm=lcl&ved=2ahUKEwjT1IzSnffmAhXn1uAKHaimC3EQjGp6BAgLEDQ&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2&rldoc=1#rlfi=hd:;tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2"
    browser.get(url)
    while True:
        try:
            card = browser.find_elements_by_class_name("cXedhc")
            review_text = browser.find_elements_by_class_name(
                "rllt__details")
           
            with tqdm(total=len(data)) as pbar:
                pbar.update(len(data) * 10)
                pbar.desc = 'scraping'
                for title in card:
                    data.append({'name':getTitle(title.text),'location':location, 'tel':getPhone(title.text)})
            browser.find_element_by_xpath("//*[@id='pnnext']").click()
            time.sleep(5)
            # WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='pnnext']")))
        except (TimeoutException, WebDriverException) as e:
            if not os.path.exists(f'{prompt}'):
                os.makedirs(f'{prompt}')
            with open(f'{prompt}/{location}.json', 'w') as file:
                json.dump(data, file)
            print(f'got {len(data)} {prompt} from {location}')
            break
