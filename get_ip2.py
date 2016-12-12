import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import time
import random
import pymongo

client = pymongo.MongoClient('localhost',27017)
ip_list = client['ip_list']
ip_info = ip_list['ip_list1']

url_test = 'http://ip.chinaz.com/getip.aspx'
# url_test = 'http://www.itjuzi.com/company/13419'
proxy_list = [
    'http://106.75.128.89:80'
    ]
proxy_ip = random.choice(proxy_list) # 随机获取代理ip
proxies_1 = {'http': proxy_ip}


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

def get_ip(url_ip):
    wb_data = requests.get(url_ip,headers=headers)
    soup = BeautifulSoup(wb_data.text,'lxml')
    ips = soup.findAll('tr')
    for x in range(1,len(ips)):
        ip = ips[x]
        tds = ip.findAll('td')
        # iplist = str(tds[1].contents[0])
        iplist= str(tds[0].contents[0]) + str(':') + str(tds[1].contents[0])
        proxy = str('http://') + iplist
        proxies = {'http': proxy}
        time.sleep(0.5)
        try:
            requests.get(url_test,proxies=proxies,timeout=0.3)
            ip_info.insert_one({'http':proxy})
            print(proxy,'验证成功！')
        except :
            print(proxy, '验证失败...')


if __name__ == '__main__':
    for i in range(1,10):
        url_ip = 'http://www.kxdaili.com/dailiip/1/{}.html#ip'.format(str(i))
        print(url_ip)
        get_ip(url_ip)