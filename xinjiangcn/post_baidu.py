import re
from requests_html import HTMLSession
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from urllib.parse import quote
import ssl
import time

ssl._create_default_https_context = ssl._create_unverified_context

base_url = 'https://www.xiaodown.com/'
wp = Client(str(base_url)+'xmlrpc.php','admin','12qwaszx')
post = WordPressPost()
post.post_status = 'publish'

post.terms_names = {
    'category':['旅游问答']
}

def htmldown(url):
    session = HTMLSession()
    html = session.get(url).html
    return html

def fabu(single_link):
    print(single_link)
    post.custom_fields = []
    post.custom_fields.append({
        'key':'via',
        'value':single_link,
    })
    html = htmldown(single_link)
    title = html.find('span.ask-title',first=True).text
    post.title = title
    print(title)

    try:
        html.find('.best-text', first=True).text
    except:
        try:
            html.find('.long-question',first=True).text
        except:
            content = ''
        else:
            content = html.find('.long-question', first=True).text
    else:
        content = html.find('.best-text', first=True).text

    try:
        html.find('.con-all',first=True).text
    except:
        try:
            html.find('.con',first=True).text
        except:
            all_content = content
        else:
            ask_content = html.find('.con', first=True).text
            all_content = str(ask_content) + '\n\n' + str(content)
    else:
        ask_content = html.find('.con-all', first=True).text
        all_content = str(ask_content) + '\n\n' + str(content)

    all_content = re.sub('\n','\n\n',all_content)
    all_content = re.sub(',','，',all_content)
    all_content = re.sub('\.','。',all_content)
    post.content = all_content.replace("展开全部","")

    # 添加特色图
    try:
        html.find('.wgt-ask .q-img-wp img.q-img-item', first=True).attrs['src']
    except AttributeError:
        post.thumbnail = None
    else:
        img = html.find('img.q-img-item', first=True).attrs['src']
        img = HTMLSession().get(img).content
        data = {'name': 'picture.jpg','type': 'image/jpeg'}
        data['bits'] = xmlrpc_client.Binary(img)
        response = wp.call(media.UploadFile(data))
        post.thumbnail = response['id']

    post.id = wp.call(posts.NewPost(post))  # 返回文章ID
    print(str(base_url)+'?p='+str(post.id))
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

def start():
    keywords=['四川','四川旅游','都江堰','青城山','乐山','九寨沟','熊猫基地','蜀南竹海','西岭雪山','川西','稻城亚丁','稻城','亚丁']
    keyword_list = []
    for keyword in keywords:
        keyword=keyword.encode('GBK','replace') # 转换为GBK
        keyword = quote(keyword) # 进行url编码
        keyword_list.append(keyword)
    return keyword_list

def run(keyword):
    # 文章计数
    max_page = 760
    num = 1
    x = 0
    while(x<max_page):
        page_url = ('https://zhidao.baidu.com/search?word='+str(keyword)+'&ie=gbk&site=-1&sites=0&date=0&pn='+str(x))
        html = htmldown(page_url)
        links = html.find('a.ti')
        for i in links:
            url = i.attrs['href']
            if 'zhidao' in url:
                try:
                    fabu(url)
                    num = num + 1
                    print('\n')
                except:
                    pass
        x = x + 10

for keyword in start():
    run(keyword)