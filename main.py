#coding=utf-8
from multiprocessing import Pool
import requests
from pages import get_links_from,get_item_info,url_list,item_info


db_url = [item['url'] for item in url_list.find()]
index_url = [item['url'] for item in item_info.find()]
x = set(db_url)
y = set(index_url)
rest_of_urls = x - y

url_channel = "http://www.itjuzi.com/company"
url_all = []

def get_all_links_from(url):
    for num in range(11,3407):
        print(num)
        get_links_from(url,num)

if __name__=='__main__':
    pool = Pool(processes=4)  #自动分配进程
    pool.map(get_all_links_from,url_channel.split())
    # for a in url_list.find({},{'url':1,'_id':0}):
    #     url_all.append(a['url'])
    # print('剩余:', len(rest_of_urls))
    # pool.map(get_item_info,rest_of_urls)
    pool.close()
    pool.join()
    # get_all_links_from(url_channel)



