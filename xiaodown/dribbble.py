from script import google_translate
from script import sql
from script import time
from requests_html import HTMLSession
import ssl

ssl._create_default_https_context=ssl._create_unverified_context

def htmldown(url):
    html = HTMLSession().get(url).html
    return html

def page_list():
    x = 1
    page_list = []
    while(x<=2):
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
            single_list.append('https://dribbble.com'+str(url)+'/attachments')
    single_list = list(set(single_list))
    return single_list

def fabu(url):
    if str(sql.sql('xiaodown','dribbble',str(url))) == 'bucunzai':
        print(time.thetime()+'新文章，开始采集 '+url)
    else:
        print(time.thetime()+'已存在跳过 '+url)

def run():
    for i in single_list():
        fabu(i)