import re
from requests_html import HTMLSession

def htmldown(url):
    html = HTMLSession().get(url).html
    return html
x=1
max_page = 13
while(x<=max_page):
    html = htmldown('https://travelsearch.fliggy.com/index.htm?searchType=product&keyword=%E6%96%B0%E7%96%86&category=GROUP_TOUR&pagenum='+str(x))
    id_list = re.findall(r'"https://traveldetail\.fliggy\.com/item\.htm\?id=([\d]+)"',html.html)
    id_list = list(set(id_list))
    print(len(id_list))
    with open('c:/python/xjcn/id.text','a') as f:
        for i in id_list:
            f.write(i+'\n')
            print(i)
    x = x+1