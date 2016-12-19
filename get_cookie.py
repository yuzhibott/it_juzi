#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pickle
import os
import time

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"]=(
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"
	)
dcap["phantomjs.page.customHeaders.Accept-Language"]=('en-US,en;q=0.8')
service_args = [
    '--proxy=127.0.0.1:9999',
    '--proxy-type=socks5',
]


def cookie_website():
	url = 'https://www.itjuzi.com/user/login'
	# webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Accept-Language'] = 'en-US'
	driver = webdriver.PhantomJS(desired_capabilities=dcap)
	driver.get('http://httpbin.org/headers')
	# print(driver.page_source)
	# print(driver.capabilities)
	driver.get(url)
	driver.find_element_by_xpath('//*[@id="create_account_email"]').send_keys('youraccount')
	driver.find_element_by_xpath('//input[@type="password"]').send_keys('yourpassword')
	driver.find_element_by_xpath('//*[@id="login_btn"]').click()

	cookie_list = driver.get_cookies()
	# print(cookie_list)

	cookie_dict = {}
	os.chdir("/home/ke/it_juzi/mycookies") 
	for cookie in cookie_list :
		f = open(cookie['name']+'.kzt','wb')
		pickle.dump(cookie,f)
		f.close()

	if 'name' in cookie and 'value' in cookie:
		cookie_dict[cookie['name']] = cookie['value']

	driver.quit()
	return cookie_dict

def cookie_notebook():
	cookie_dict = {}
	for parent,dirnames,filenames in os.walk('./mycookies'):
		for filename in filenames:
			if filename.endswith('.kzt'):
				print(filename)
				with open(filename,'rb+') as f:
					d = pickle.load(f)

					if 'name' in d and 'value' in d and 'expiry' in d:
						expiry_date = int(d['expiry'])
						if expiry_date > (int)(time.time()):
							cookie_dict[d['name']] = d['value']
						else:
							return {}
	return cookie_dict

def get_cookie():
	cookie_dict = cookie_notebook()
	if not cookie_dict:
		cookie_dict = cookie_website()

	return cookie_dict

cookie_website()