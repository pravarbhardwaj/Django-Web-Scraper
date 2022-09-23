from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrapper():
    dic = {}
    chromeOptions = Options()
    chromeOptions.add_argument('--disable-logging')
    chromeOptions.headless = True
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chromeOptions)
    driver.get("https://www.airtel.in/myplan-infinity/")
    table = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/section/div/div[1]')
    attri = table.get_attribute('innerHTML')
    driver.close()
    soup = BeautifulSoup(attri, features="lxml")
    mydivs = soup.find_all("div", {"class": "single_cart"})
    for div in mydivs:
        monthly_plan = div.find("span", {"class": "price"})
        more_divs = div.find_all("div", {"class": "border-bottom"})
        benefits = []
        for a in more_divs:
            benefits.append(a.find("span").get_text())
        dic[monthly_plan.get_text()] = {'monthly_plan': monthly_plan, 'data_with_rollover': benefits[0], 'sms_per_day': benefits[1], 'local_std_roaming': benefits[2], 'amazon_prime': benefits[3]}
    return dic