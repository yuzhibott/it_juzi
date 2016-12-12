#coding=utf-8
from bs4 import BeautifulSoup
import requests
import time
import  pymongo
import random

# 在最左边是在python 中对象的名称，后面的是在数据库中的名称
client = pymongo.MongoClient('localhost',27017)
itorange = client['itorange']
url_list = itorange['url_itorange']
item_info = itorange['item_itorange']
ip_list = client['ip_list']
my_iplist = ip_list['ip_list2']

ip_all = []
for a in my_iplist.find({},{'http':1,'_id':0}):
    ip_all.append(a)

proxy_list = [
      # 'http://106.75.128.89:80'
      'http://182.90.33.7:80'
    ]
# proxy_ip = random.choice(proxy_list) # 随机获取代理ip
# proxies = {'http': proxy_ip}

headers_1 = \
    {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Cookie':'gr_user_id=72f30897-e2a7-4ebd-a4b6-36559bdab076; identity=kzt120707%40163.com; remember_code=LrMY6B82uN; acw_tc=AQAAANZZtmPSagEAWgJJ36MyrjaR7b6n; session=3b59476b105beb94e3985da08c1b414f888fbeea; acw_sc=5814082bf6d44062410b7ddc26cbcdf766d859bd; _gat=1; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1477212179,1477311499,1477577809,1477707820; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1477708065; gr_session_id_eee5a46c52000d401f969f4535bdaa78=c2b1f94e-9308-4430-ba85-11f9552202df; _ga=GA1.2.1785082626.1476178721',
        'Connection':'keep-alive',
        # 'Host':'www.itjuzi.com',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Upgrade-Insecure-Requests':'1'
    }

headers_2 = {
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E)',
        'Cookie':'id58=c5/nq1fjkOcJsSoDAw3UAg==; als=0; myfeet_tooltip=end; __utma=253535702.1803438396.1474552057.1474552057.1474552057.1; __utmz=253535702.1474552057.1.1.utmcsr=huizhou.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/sale.shtml; sz=2016922214738; bj58_id58s=UXdTbFROcHhTeDJrODA3Nw==; ipcity=gz%7C%u5E7F%u5DDE%7C0; sessionid=fb8b8e5d-e90b-4efd-a344-9a71d16b57b6; final_history=27493512474798%2C27362536768303%2C26808000060980; 58home=sz; city=sz; bj58_new_session=0; bj58_init_refer=http://sz.58.com/; bj58_new_uv=8; 58tj_uuid=724261e6-8115-4cb5-9db6-d20e28cc23d9; new_session=0; new_uv=11; utm_source=; spm=; init_refer=http%253A%252F%252Fsz.58.com%252F',
        'Host':'www.itjuzi.com'
}


#spider 1
def get_links_from(url,pages):
    list_view = '{}?page={}'.format(url,str(pages))
    headers_1.update({'Referer':list_view})
    proxies = random.choice(ip_all)
    stime = random.randint(1,3)
    time.sleep(stime)
    wb_data = requests.get(list_view,headers=headers_1,timeout=5)
    soup = BeautifulSoup(wb_data.text,'lxml')
    if soup.find('p','title'):
        for link in soup.select('p.title a'):
            item_link = link.get('href')
            # url_list.insert_one({'url':item_link})
            print(item_link)

#spider 2
def get_item_info(url):
    # print(url)
    # print(proxies)
    headers_1.update({'Referer': url})
    proxies = random.choice(ip_all)
    stime =random.randint(1,3)
    time.sleep(stime)
    try:
        wb_data = requests.get(url,headers=headers_1,timeout=3,proxies=proxies)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        data = {
            'name':soup.title.text.split(' ')[0],
            'financing':soup.select(' div > div.picinfo > div.line-title > span.title > b > span')[0].text.strip().replace('(','').replace(')',''),
            'scope':list(map(lambda x:x.text,soup.select('div.rowhead > div.picinfo > div > span.scope.c-gray-aset > a:nth-of-type(1)'))),
            'sec_scope':list(map(lambda x:x.text,soup.select('div.rowhead > div.picinfo > div > span.scope.c-gray-aset > a:nth-of-type(2)'))),
            'city':list(soup.select('div.rowhead > div.picinfo > div:nth-of-type(3) > span.loca.c-gray-aset')[0].stripped_strings),
            'date':list(map(lambda x:x.text.split('：')[1],soup.select('div.block-inc-info.on-edit-hide >  div > div:nth-of-type(2) > span:nth-of-type(1)'))),
            'status':soup.select('div.sec.ugc-block-item.bgpink > div.block-inc-info.on-edit-hide > div > div:nth-of-type(3) > span')[0].text,
            'url':url
        }
        print(data)
        item_info.insert_one(data)
    except:
        # print(proxies)
        ip_list.ip_list2.remove(proxies)
        # print('更换ip...')


get_links_from('http://www.itjuzi.com/company',7)
#get_item_info('http://www.itjuzi.com/company/4773')



