import sys
import os
import re
import google_translate
import sql
import xd_time
from requests_html import HTMLSession
import ssl
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc import WordPressTerm
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

ssl._create_default_https_context=ssl._create_unverified_context

def htmldown(url):
    html = HTMLSession().get(url).html
    return html

def page_list():
    x = 1
    page_list = []
    while(x<=5):
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
    return single_list

def fabu(url):
    wp = Client('https://www.xiaodown.com/xmlrpc.php', 'admin', '12qwaszx')
    post = WordPressPost()
    post.post_status = 'publish'
    print('\n')
    print(xd_time.thetime()+'发现文章：'+url)

    html = htmldown(url)

    post.custom_fields = []
    post.terms_names = {}

    post.terms_names['category'] = ['素材']

    # url写入自定义字段
    post.custom_fields.append({
        'key':'via',
        'value':str(url)
    })

    # 标题
    try:
        title = html.find('h1.shot-title')[0].text
    except:
        pass
    else:
        title = google_translate.en_to_cn(title)
        post.title = str(title)
        print(xd_time.thetime()+'开始采集：'+title)

    # 内容
    try:
        content = html.find('.shot-desc')[0].text
    except:
        pass
    else:
        content = google_translate.en_to_cn(content)
        content = re.sub('\n','\n\n',content)
        post.content = str(content)
        # print(content)

    # 标签
    try:
        tag = html.find('.shot-tags ol')[0].find('li a')
    except:
        pass
    else:
        tag_list_text =''
        for i in tag:
            tag_list_text = tag_list_text + str(i.text) + ','
        tag_list_text = google_translate.en_to_cn(tag_list_text)
        tag_list = tag_list_text.split('，')
        tag_list = list(filter(None,tag_list))
        post.terms_names['post_tag'] = tag_list
        # print(tag_list)

    # 颜色
    try:
        color = html.find('.shot-colors ul')[0].find('li a')
    except:
        pass
    else:
        color_list = ''
        for i in color:
            color_list = color_list + str(i.text) + ','
        post.custom_fields.append({
            'key':'color',
            'value':color_list
        })
        # print(color_list)

    # 特色图片
    try:
        thumb = html.find('.main-shot .detail-shot')[0].attrs['data-img-src']
    except:
        pass
    else:
        img = HTMLSession().get(thumb).content
        name = os.path.basename(thumb)
        data = {'name':name,'type':'image/jpeg'}
        data['bits'] = xmlrpc_client.Binary(img)
        response = wp.call(media.UploadFile(data))
        post.thumbnail = response['id']
        # print(response['url'])

    post.id = wp.call(posts.NewPost(post))
    print(xd_time.thetime()+'发布返回ID：'+str(post.id))

def run():
    for url in single_list():
        if str(sql.sql_chaxun('xiaodown', 'dribbble', str(url))) == 'bucunzai':
            fabu(url)
            sql.sql_charu('xiaodown','dribbble',str(url))
            print(xd_time.thetime() + '插入数据库：'+url)
            print('\n')
        else:
            print(xd_time.thetime() + '已存在跳过：' + url)
            print('\n')