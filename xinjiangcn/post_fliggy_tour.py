from selenium import webdriver
from requests_html import HTML
import time

def htmldown(url):
    brower = webdriver.Chrome()
    brower.set_window_size(100,200)
    brower.get(url)

    time.sleep(3)

    js = "document.documentElement.scrollTop=10000"
    brower.execute_script(js)

    time.sleep(1)

    js = "document.documentElement.scrollTop=10000"
    brower.execute_script(js)

    time.sleep(3)

    html = brower.page_source
    html = HTML(html=html)
    return html

def fabu(url):
    html = htmldown(url)
    jiage = html.find('.mod-price-desc')[0].text
    print(jiage)

fabu('https://h5.m.taobao.com/trip/travel-detail/index/index.html?&id=578511292143')