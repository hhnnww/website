from script import google_translate
from requests_html import HTMLSession
import ssl
import time

ssl._create_default_https_context=ssl._create_unverified_context
time = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

def htmldown(url):
    html = HTMLSession().get(url).html
    return html

def page_list():
    x = 1
    page_list = []
    while(x<=20):
        page_list.append('https://dribbble.com/?per_page=24&page='+str(x))
        x = x +1
    return page_list

def single_list():
    single_list = []
    for i in page_list():
        html = htmldown(i)
        url = html.find('.dribbble-over')
        for i in url:
            url = i.attrs['href']
            single_list.append('https://dribbble.com'+str(url))
    single_list = list(set(single_list))
    print(time+'发现页面：'+str(len(single_list)))
    return single_list

single_list()