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


ls = ['Kigali','Bugesera',
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
def getLocation(t):
    l = t.split('\n')[-2]
    if l in ls:
        return l
    else:
        return 'No address'
     
def getTitle(t):
    return t.split('\n')[0].strip()

def getPhone(t):
    p = t.split('⋅')[-1].split('·')[-1].replace(" ", "")
    if isPhoneNumber(p):
        return p
    else:
        return 'No phone number'

def app():
    n = str(input("What are you looking for?: "))
    q = n.replace(" ", "+")
    options = webdriver.ChromeOptions()

    options.add_argument('headless')

    browser = webdriver.Chrome(options=options)

    d=[]

    u = f"https://www.google.com/search?sxsrf=ACYBGNTuYn04lHdVfa6QBkoHVHDxaEfr0Q:1578597416649&q={q}&npsic=0&rflfq=1&rlha=0&tbm=lcl&ved=2ahUKEwjT1IzSnffmAhXn1uAKHaimC3EQjGp6BAgLEDQ&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2&rldoc=1#rlfi=hd:;tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2"
    browser.get(u)
    while True:
        try:
            p = browser.find_elements_by_class_name("pn")
            c = browser.find_elements_by_class_name("cXedhc")
            review_text = browser.find_elements_by_class_name(
                "rllt__details")
           
            with tqdm(total=len(d)) as pbar:
                pbar.update(len(d) / 0.1)
                pbar.desc = 'scraping'
                for title in c:
                    
                    d.append({'name':getTitle(title.text),'location':getLocation(title.text), 'tel':getPhone(title.text)})
            browser.find_element_by_xpath("//*[@id='pnnext']").click()
            time.sleep(5)
            # WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='pnnext']")))
        except (TimeoutException, WebDriverException) as e:
            with open(f'{n}.json', 'w') as file:
                json.dump(d, file)
            print(f'got {len(d)} {n} in total')
            break
