from pre.settings import DownLoad_Path, Final_Path, BackUp_Path
from pre.get_useragent import getUserAgent
from pre.get_proxy import get_random_ip, get_proxy
from bs4 import BeautifulSoup
import os
import sys
import requests
import random


class VideoClawer_1024():
    def __init__(self):
        self.headers = {
            'User-Agent': getUserAgent()
        }
        self.movies_url = []
        self.proxies = {}
        self.id = ""
        self.filename = Final_Path+"\\tmp.mp4"

    def start(self, url):
        html = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(html.content, 'lxml')
        # 文件名获取
        _node = soup.find(id="subject_tpc")
        self.filename = Final_Path+"\\"+_node.text + ".mp4"
        # ID获取
        node = soup.find(name='iframe')
        src = node.attrs['src']
        _src = src.split('/')
        self.id = _src[-1][4:]
        _url = "https://m3u8.cdnpan.com/"+self.id+".m3u8"
        self.get_url(_url)

    def get_url(self, _url):

        all_url = _url.split('/')
        url_next = BackUp_Path + "\\" + all_url[-1]

        # 获取m3u8文件
        m3u8_txt = requests.get(_url, headers=self.headers)
        with open(url_next, 'wb') as m3u8_content:
            m3u8_content.write(m3u8_txt.content)
        # 提取ts视频的url
        _urls = open(url_next, 'r')
        for line in _urls.readlines():
            if '.ts' in line:
                self.movies_url.append(line[:-1])
            else:
                continue
        # print(self.movies_url)
        _urls.close()
        self.startDownLoad()

    def startDownLoad(self):
        print("开始下载")
        flag = 0
        ip_list = get_proxy()
        total_size = int(len(self.movies_url))
        temp_size = 0
        while self.movies_url:
            self.headers = {
                'User-Agent': getUserAgent()
            }
            url = self.movies_url.pop()
            _url = url.split('/')
            filename = _url[-1]
            Fullname = DownLoad_Path + "\\" + filename
            print("正在下载"+filename+"...")
            while True:
                try:
                    if flag == 0:
                        ts = requests.get(url, headers=self.headers)
                    else:
                        ts = requests.get(url, headers=self.headers, proxies=self.proxies)
                    with open(Fullname, 'wb') as f:
                        f.write(ts.content)
                    done = int(50 * temp_size / total_size)
                    temp_size += 1
                    sys.stdout.write("\r[%s%s] %d%%" % ('▮' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                    sys.stdout.flush()
                    break
                except requests.ConnectionError:
                    print('Error')
                    proxy = get_random_ip(ip_list)
                    self.proxies = {'http': proxy,
                               'https': proxy}
                    continue

    def parese_data(self):
        print()
        print("开始合并")
        files = os.listdir(DownLoad_Path)
        # 合并
        with open(self.filename, 'wb+') as  w:
            for file in files:
                Combine_file = DownLoad_Path + '\\' + file
                with open(Combine_file, 'rb') as r:
                    w.write(r.read())
                os.remove(Combine_file)
        print("合并完成")


if __name__ == '__main__':
    a = VideoClawer_1024()
    url = input("输入网址:")
    a.start(url)
    a.parese_data()