from django.shortcuts import render
from jio.models import Jio
from .serializers import JioSerializers
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from rest_framework import viewsets
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rest_framework.decorators import api_view
from rest_framework.response import Response


def index(request):
    data = Jio.objects.all()
    myData = {'jio_data': data}
    return render(request, 'jio/jioIndex.html', context=myData)

@api_view(['GET'])
def data(request):
    jio = Jio.objects.all()
    serializer = JioSerializers(jio, many=True)
    return Response(serializer.data)

class JioViewSet(viewsets.ModelViewSet):

    serializer_class = JioSerializers

    def get_queryset_data(self):
        data = Jio.objects.all()
        return data

    def _get_jio_data(self):
        dic = {}
        chromeOptions = Options()

        chromeOptions.add_argument("window-size=1400x900")
        chromeOptions.add_argument('--disable-logging')
        chromeOptions.add_argument('--disable-extensions')
        chromeOptions.add_argument('--disable-in-process-stack-traces')
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('--log-level=3')
        chromeOptions.headless = True
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)
        driver.maximize_window()
        driver.get("https://www.jio.com/selfcare/plans/mobility/postpaid-plans-list/?category=Main%20Plan&categoryId=TWFpbiBQbGFu")
        try:
            found = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/section[1]/div[2]/button')
            found.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/section[1]/div[3]/div[2]/div[5]/div/section'))
            )
            all_plans = driver.find_elements(By.CLASS_NAME, 'planDetailsCard_container__1gH8d')
            for i in range(len(all_plans)):
                plan_details = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[2]/section[1]/div[3]/div[2]/div[{i+1}]/div/section/div/div[2]/div/div[2]/div/div[4]/div[3]/button[2]')
                plan_details.click()
                details_presence = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div'))
                )
                plan_data = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[2]/div/div/div')
                
                plan_data = plan_data.get_attribute('innerHTML')
                soup = BeautifulSoup(plan_data, features="lxml")
                values = soup.find_all("div", {"class": "detailsTable_detailsRow__2DKYX"})
                benefits = []
                for val in values:
                    benefits.append(val.text)
                dic[benefits[0].replace("₹", "")] = {'monthly_plan': benefits[0], 'pack_validity': benefits[1], 'total_data': benefits[2],
                'data_roll_over': benefits[3], 'family_plan_additional_sim_cards': benefits[4], 'voice_call': benefits[5], 
                'sms': benefits[6], 'netflix_mobile': 'NO', 'jio_tv': 'NO', 'amazon_prime': 'NO', 'jio_cloud': 'NO', 'jio_security': 'NO'}
                added_benefits = soup.find_all("div", {"class": "j-text j-text-body-xxs"})
                for benefit in added_benefits:
                    selected_dic = dic[benefits[0].replace("₹", "")]
                    if benefit.text == 'Netflix)Mobile paln' or 'Netflix(Mobile plan)':
                        selected_dic['netflix_mobile'] = 'YES'
                    if benefit.text == 'Amazon Prime':
                        selected_dic['amazon_prime'] = 'YES'
                    if benefit.text == 'JioTV':
                        selected_dic['jio_tv'] = 'YES'
                    if benefit.text == 'JioSecurity':
                        selected_dic['jio_security'] = 'YES'
                    if benefit.text == 'JioCloud':
                        selected_dic['jio_cloud'] = 'YES'
                plans_details_close = driver.find_element(By.XPATH, f'/html/body/div[2]/div/div/header/button')
                plans_details_close.click()
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/section[1]/div[3]/div[2]/div[5]/div/section'))
            )
        except IndexError:
            pass
        finally:
            driver.quit()
        if dic:
            self.delete_data()
        return dic

    def save_data(self):
        jio_data = self._get_jio_data()
        if jio_data is not None:
            try:
                for data in jio_data:
                    jio_object = Jio.objects.create(monthly_rental=jio_data[data]['monthly_plan'], voice_call=jio_data[data]['voice_call'],
                    data_with_rollover=jio_data[data]['data_roll_over'], 
                    sms_per_day=jio_data[data]['sms'],
                    family_plan=jio_data[data]['family_plan_additional_sim_cards'], 
                    pack_validity=jio_data[data]['pack_validity'], total_data=jio_data[data]['total_data'],
                    amazon_prime=jio_data[data]['amazon_prime'], netflix_mobile=jio_data[data]['netflix_mobile'],
                    jio_cloud=jio_data[data]['jio_cloud'], jio_tv=jio_data[data]['jio_tv'],
                    jio_security=jio_data[data]['jio_security'])
                    jio_object.save()
                print("General Log - Data added successfully for JIO!")
            except Exception as e:
                print(e)
                pass

    def delete_data(self):
        Jio.objects.all().delete()
        print('General Log - Data deleted successfully for Jio')
