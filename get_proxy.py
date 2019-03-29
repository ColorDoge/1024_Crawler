import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
PROXY_POOL_URL = 'http://localhost:5555/random'


def getProxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            #print("GET_Proxy: "+response.text)
            return response.text
    except ConnectionError:
        print('ConnectionError')
        return None


def get_ip_list(obj):
    ip_text = obj.findAll('tr', {'class': 'odd'})   # 获取带有IP地址的表格的所有行
    ip_list = []
    for i in range(len(ip_text)):
        ip_tag = ip_text[i].findAll('td')
        ip_port = ip_tag[1].get_text() + ':' + ip_tag[2].get_text() # 提取出IP地址和端口号
        ip_list.append(ip_port)
    # print("共收集到了{}个代理IP".format(len(ip_list)))
    # print(ip_list)
    return ip_list


def get_random_ip(ip_list):
    import random
    return random.choice(ip_list)

def get_proxy():
    url = 'https://www.xicidaili.com/'
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    request = Request(url, headers=headers)
    response = urlopen(request)
    bsObj = BeautifulSoup(response, 'lxml')
    ip_list = get_ip_list(bsObj)
    return ip_list

if __name__ == '__main__':
    print(get_proxy())
