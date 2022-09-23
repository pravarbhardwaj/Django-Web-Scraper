from django.shortcuts import render
from django.http import JsonResponse
from airtel.models import Airtel
from .serializers import AirtelSerializer
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from rest_framework import viewsets
from webdriver_manager.chrome import ChromeDriverManager


def index(request):
    data = Airtel.objects.all()
    myData = {'airtel_data': data}
    return render(request, 'airtel/index.html', context=myData)

def data(request):
    airtel = Airtel.objects.all()
    serializer = AirtelSerializer(airtel, many=True)
    return JsonResponse(serializer.data, safe=False)

class AirtelViewSet(viewsets.ModelViewSet):

    serializer_class = AirtelSerializer

    def get_queryset_data(self):
        data = Airtel.objects.all()
        return data

    def _get_airtel_data(self):
        dic = {}
        chromeOptions = Options()
        chromeOptions.add_argument('--disable-logging')
        chromeOptions.headless = True
        prefs = {"profile.managed_default_content_settings.images": 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)
        driver.get("https://www.airtel.in/myplan-infinity/")
        table = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/section/div/div[1]')
        attri = table.get_attribute('innerHTML')
        driver.close()
        try:
            soup = BeautifulSoup(attri, features="lxml")
            mydivs = soup.find_all("div", {"class": "single_cart"})
            for div in mydivs:
                monthly_plan = div.find("span", {"class": "price"})
                more_divs = div.find_all("div", {"class": "border-bottom"})
                benefits = []
                for a in more_divs:
                    benefits.append(a.find("span").get_text())
                dic[monthly_plan.get_text()] = {'monthly_plan': monthly_plan.get_text(), 
                'data_with_rollover': benefits[0], 'sms_per_day': benefits[1], 'local_std_roaming': benefits[2], 'amazon_prime': benefits[3]}
            self.delete_data()
            return dic
        except Exception as e:
            print(e)
            return None

    def save_data(self):
        airtel_data = self._get_airtel_data()
        if airtel_data is not None:
            try:
                for data in airtel_data:
                    airtel_object = Airtel.objects.create(monthly_rental=airtel_data[data]['monthly_plan'], data_with_rollover=airtel_data[data]['data_with_rollover'], 
                    sms_per_day=airtel_data[data]['sms_per_day'], local_std_roaming=airtel_data[data]['local_std_roaming'], 
                    amazon_prime=airtel_data[data]['amazon_prime'])
                    airtel_object.save()
                print("General Log - Data added successfully!")
            except Exception as e:
                print(e)
                pass

    def delete_data(self):
        Airtel.objects.all().delete()
        print('General Log - Data deleted successfully')
