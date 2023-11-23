import requests
from datetime import datetime
from bs4 import BeautifulSoup

def get_weather_data():
    
    # enter city name
    city = "Banja Luka"
    
    # create url
    url = "https://www.google.com/search?q="+"weather"+city
    
    # requests instance
    html = requests.get(url).content
    
    # getting raw data
    soup = BeautifulSoup(html, 'html.parser')


    # get the temperature
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    
    # this contains time and sky description
    time_and_sky = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    
    # format the data
    time = time_and_sky.split('\n')[0]
    dan = time.split(" ")[0].capitalize()
    vrijeme = time.split(" ")[1]
    sky = time_and_sky.split('\n')[1]
    datum = datetime.now()
    datum = datum.strftime("%d.%m.%Y")

    return datum, dan, vrijeme, sky, temp
