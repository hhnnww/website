import hashlib
import sys
import os
import re
import google_translate
import xd_sql
import xd_time
from requests_html import HTMLSession
import ssl
import time
import datetime
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

def imgup(url):
    
    img = HTMLSession().get(url).content
    on_time = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    
    name = os.path.basename(url)
    name = on_time+'_'+name
    
    year = str(time.strftime('%Y'))
    month = str(time.strftime('%m'))
    
    file_path = 'C:\\xampp\\htdocs\\wp-content\\uploads\\'+year+'\\'+month+'\\'+name

    with open('C:\\xampp\\htdocs\\wp-content\\uploads\\'+year+'\\'+month+'\\'+name,'wb') as f:
        f.write(img)
    return 'http://127.0.0.1/wp-content/uploads/'+year+'/'+month+'/'+name

def shuchu(text,link):
    print(xd_time.thetime()+text+':'+link)

def fabu(url):
    
    wp = Client('http://127.0.0.1/xmlrpc.php', 'admin', '111')
    post = WordPressPost()
    post.post_status = 'publish'

    shuchu('发现文章',url)

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
        shuchu('开始采集',title)

    # 内容
    try:
        content = html.find('.shot-desc')[0].text
    except:
        post.content = ''
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
        shuchu('上传特色图成功',response['url'])

    # 附件
    img_type = html.find('.main-shot')[0].attrs['class']

    # 如果是MP4文件，直接获取
    if 'video' in img_type:
        mp4 = html.find('.detail-shot .video-container video')[0].attrs['src']
        att = imgup(mp4)
        post.custom_fields.append({
            'key':'type',
            'value':'mp4'
            })
        post.custom_fields.append({
            'key':'att',
            'value':att
            })
        shuchu('mp4附件',att)
    else:
        # 如果是图片
        post.custom_fields.append({
            'key':'type',
            'value':'img'
            })

        try:
            # 判断是否存在附件页面
            att_url = html.find('.main-shot .detail-shot a')[0].attrs['href']
        except:
            # 如果不存在附件页面，直接抓取当页图片
            att = html.find('.main-shot .detail-shot img')[0].attrs['src']
            att = imgup(att)
            post.custom_fields.append({
                'key':'att',
                'value':att
                })
            shuchu('单张图片附件',att)
        else:
            # 开始载入附件页面进行分析
            att_url = 'https://dribbble.com'+str(att_url)
            att_html = htmldown(att_url)
            try:
                # 判断附件是否有ul多张图片
                img_list = att_html.find('#attachments ul')[0].find('li')
            except:
                # 如果附件页面只有一张图
                att = att_html.find('#viewer #viewer-img img')[0].attrs['src']
                att = imgup(att)
                post.custom_fields.append({
                    'key':'att',
                    'value':att
                    })
                shuchu('单张图片附件',att)

            else:
                # 如果附件页面存在ul有多张图片
                att = response['url']
                for i in img_list[1:]:
                    img = i.find('a img')[0].attrs['src']
                    img = re.sub(r'\/thumbnail','',img)
                    single_att = imgup(img)
                    att = str(single_att)+','+att
                shuchu('多张图片附件',att)
                post.custom_fields.append({
                    'key':'att',
                    'value':att
                    })

    post.id = wp.call(posts.NewPost(post))
    shuchu('发布成功',post.id)

def run():
    for url in single_list():
        if str(xd_sql.sql_chaxun('xiaodown', 'dribbble', str(url))) == 'bucunzai':
            fabu(url)
            # xd_sql.sql_charu('xiaodown','dribbble',str(url))
            # shuchu('插入到mysql去重','')
            print('\n\n')
        else:
            shuchu('已存在跳过',url)
            print('\n\n')