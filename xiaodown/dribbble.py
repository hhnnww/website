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

# 下载模块
def htmldown(url):
    html = HTMLSession().get(url).html
    return html

# 生成列表页函数
def page_list():
    x = 1
    page_list = []
    while(x<=2):
        page_list.append('https://dribbble.com/?per_page=24&page='+str(x))
        x = x +1
    return page_list

# 从列表页中生成单页函数
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


# 图片直接上传函数
def imgup(url):
    
    img = HTMLSession().get(url).content
    on_time = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    
    name = os.path.basename(url)
    name = re.sub(r'.*?\.','.',name)
    name = on_time+name
    
    year = str(time.strftime('%Y'))
    month = str(time.strftime('%m'))

    if os.path.exists('C:\\xampp\\htdocs\\wp-content\\uploads\\'+year) == False:
        os.mkdir('C:\\xampp\\htdocs\\wp-content\\uploads\\'+year)

    if os.path.exists('C:\\xampp\\htdocs\\wp-content\\uploads\\'+year+'\\'+month) == False:
        os.mkdir('C:\\xampp\\htdocs\\wp-content\\uploads\\'+year+'\\'+month)
    
    file_path = 'C:\\xampp\\htdocs\\wp-content\\uploads\\'+year+'\\'+month+'\\'+name

    with open('C:\\xampp\\htdocs\\wp-content\\uploads\\'+year+'\\'+month+'\\'+name,'wb') as f:
        f.write(img)

    time.sleep(1)
    return 'http://127.0.0.1/wp-content/uploads/'+year+'/'+month+'/'+name

# 格式化打印函数
def shuchu(text,link):
    print(xd_time.thetime()+text+':'+str(link))

# 文章解析发布函数
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
        post.title = str(title)
        shuchu('开始采集',title)

    # 内容
    try:
        content = html.find('.shot-desc')[0].text
    except:
        post.content = ''
    else:
        post.content = str(content)

    # 标签
    try:
        tag = html.find('.shot-tags ol')[0].find('li a')
    except:
        pass
    else:
        tag_list_text =''
        for i in tag:
            tag_list_text = tag_list_text + str(i.text) + ','
        tag_list = tag_list_text.split(',')
        tag_list = list(filter(None,tag_list))
        post.terms_names['post_tag'] = tag_list
        shuchu('标签',tag_list)

    # 颜色
    try:
        color = html.find('.shot-colors ul')[0].find('li a')
    except:
        pass
    else:
        color_list = ''
        for i in color:
            color_list = color_list + str(i.text) + ','
        color_list = color_list[:-1]
        post.custom_fields.append({
            'key':'color',
            'value':color_list
        })
        shuchu('颜色',color_list)

    # 特色图片
    try:
        thumb = html.find('.main-shot .detail-shot')[0].attrs['data-img-src']
    except:
        pass
    else:
        ts_att = imgup(thumb)
        post.custom_fields.append({
            'key':'thumb',
            'value':ts_att
            })
        shuchu('特色图片',ts_att)

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
            post.custom_fields.append({
                'key':'att',
                'value':ts_att
                })
            shuchu('没有附件，采用特色图',ts_att)
        else:
            # 开始载入附件页面进行分析
            att_url = 'https://dribbble.com'+str(att_url)
            att_html = htmldown(att_url)
            try:
                # 判断附件是否有ul多张图片
                img_list = att_html.find('#attachments ul')[0].find('li')
            except:
                # 如果附件页面只有一张图
                post.custom_fields.append({
                    'key':'att',
                    'value':ts_att
                    })
                shuchu('附件页只有一张图，采用特色图',ts_att)
            else:
                # 如果附件页面存在ul有多张图片
                att = str(ts_att)
                for i in img_list:
                    if str(i.find('a img')[0].attrs['src']) == str(thumb):
                        shuchu('附件与特色图相同','跳过')
                    else:
                        img = i.find('a img')[0].attrs['src']
                        img = re.sub(r'\/thumbnail','',img)
                        single_att = imgup(img)
                        att = att+','+str(single_att)
                shuchu('多张图片附件',att)
                post.custom_fields.append({
                    'key':'att',
                    'value':att
                    })

    post.id = wp.call(posts.NewPost(post))
    shuchu('发布成功','http://127.0.0.1/?p='+str(post.id))

def run():
    for url in single_list():
        if str(xd_sql.sql_chaxun('xiaodown', 'dribbble', str(url))) == 'bucunzai':
            try:
                fabu(url)
            except:
                shuchu('发布错误','跳过')
                return
            else:
                xd_sql.sql_charu('xiaodown','dribbble',str(url))
                shuchu('插入到mysql去重','成功')
                print('\n\n')
        else:
            shuchu('已存在跳过',url)
            print('\n\n')