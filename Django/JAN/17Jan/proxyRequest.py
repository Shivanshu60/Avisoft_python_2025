import requests
import random
from bs4 import BeautifulSoup as bs
import traceback

def get_free_proxies():

    url = "https://free-proxy-list.net/"
    soup = bs(requests.get(url).content, 'html.parser')

    # to store proxies
    proxies = []
    for row in soup.find("table", attrs={"class": "table"}).find_all("tr")[1:]:

        tds = row.find_all("td")
        try:
            ip =  tds[0].text.strip()
            port = tds[1].text.strip()
            proxies.append(str(ip) + ":"  + str(port))
        except IndexError:
            continue
    return proxies

url = "https://free-proxy-list.net/"
proxies = get_free_proxies()



for i in range(len(proxies)):
    print("Request Number:" + str(i+1))
    proxy = proxies[i]

    try:

        response = requests.get(url, proxies = {"http": proxy, "https":proxy })
        print(response.json())

    except:
        print("Not Available")

    
