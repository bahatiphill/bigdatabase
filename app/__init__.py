"""
Author: Igwaneza Bruce <knowbeeinc@gmail.com>
Attempt to collect all clinics found in rwanda,
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

# pharmacies = "https://www.google.com/search?sz=0&tbm=lcl&sxsrf=ACYBGNTSoMYKH3ThZFHsuSHTysyGkmJE6g%3A1578507952220&ei=sB4WXp6VDYvAgwfxia-QDA&q=rwanda&oq=pharmacies+in+rwanda&gs_l=psy-ab.3..0j0i5i30k1l3j0i7i5i30k1j0i8i30k1.1992468.1997458.0.1998248.10.10.0.0.0.0.317.1572.2-5j1.6.0....0...1c.1.64.psy-ab..4.6.1566...0i7i30k1j0i8i7i30k1.0.ccrkZd9VqhI#rlfi=hd:;si:;mv:[[-1.8952418999999998,30.1504698],[-2.6674822,29.7133026]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!2m1!1e3!3sIAE,lf:1,lf_ui:3"
# clinics = "https://www.google.com/search?sz=0&tbm=lcl&sxsrf=ACYBGNSiys3uXuX_0XywfYSpV74dSdepUA%3A1578507941106&ei=pR4WXq2EBsWWjLsPj7GZiAs&q=clinics+in+rwanda&oq=clinics+in+rwanda&gs_l=psy-ab.12...0.0.0.9635.0.0.0.0.0.0.0.0..0.0....0...1c..64.psy-ab..0.0.0....0.1HfVGiEW-vU#rlfi=hd:;si:;mv:[[-1.425354,30.188343699999997],[-2.6640878,29.7141865]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2"
# hospitals = "https://www.google.com/search?sz=0&tbm=lcl&sxsrf=ACYBGNSD7cdkvBn6wCB0NvQFNqpCK5Si5A%3A1578510152499&ei=SCcWXsKHHquAjLsPqJuFuAM&q=hospitals+in+rwanda&oq=hospitals+in+rwanda&gs_l=psy-ab.3..0i7i30k1l10.16320.19310.0.19500.13.11.2.0.0.0.294.1262.2-5.5.0....0...1c.1.64.psy-ab..6.4.769....0.y1HwwXxkvbg#rlfi=hd:;si:;mv:[[-1.626744,30.4595543],[-2.6666396,29.060083899999995]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2"
def getTitle(t):
    return t.split('\n')[0].strip()

def getPhone(t):
    phone = t.split('⋅')[-1].split('·')[-1].replace(" ", "")
    if isPhoneNumber(phone):
        return phone
    else:
        return 'No phone number'

def app():
    name = str(input("What are you looking for?: "))
    query = name.replace(" ", "+")
    options = webdriver.ChromeOptions()

    # options.add_argument('headless')

    browser = webdriver.Chrome(options=options)

    data=[]

    url = "https://www.google.com/search?sz=0&tbm=lcl&sxsrf=ACYBGNSD7cdkvBn6wCB0NvQFNqpCK5Si5A%3A1578510152499&ei=SCcWXsKHHquAjLsPqJuFuAM&q=" + str(query) + "&oq=" + str(query) + "&gs_l=psy-ab.3..0i7i30k1l10.16320.19310.0.19500.13.11.2.0.0.0.294.1262.2-5.5.0....0...1c.1.64.psy-ab..6.4.769....0.y1HwwXxkvbg#rlfi=hd:;si:;mv:[[-1.626744,30.4595543],[-2.6666396,29.060083899999995]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2"
    browser.get(url)
    while True:
        try:
            page = browser.find_elements_by_class_name("pn")
            clinics = browser.find_elements_by_class_name("cXedhc")
            review_text = browser.find_elements_by_class_name(
                "rllt__details")
           
            with tqdm(total=len(data)) as pbar:
                pbar.update(len(data) / 0.1)
                pbar.desc = 'scraping'
                for title in clinics:
                    data.append({'name':getTitle(title.text), 'tel':getPhone(title.text)})
            browser.find_element_by_xpath("//*[@id='pnnext']").click()
            time.sleep(5)
            # WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='pnnext']")))
        except (TimeoutException, WebDriverException) as e:
            with open(f'{name}.json', 'w') as file:
                json.dump(data, file)
            print(f'got {len(data)} {name} in total')
            break
