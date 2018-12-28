import os
import time
from requests_html import HTMLSession
import re
import hashlib
import os
import hashlib
import datetime
import re


def htmldown(url):
	html = HTMLSession().get(url).html
	return html

url = 'https://cdn.dribbble.com/users/471034/videos/6522/best6.mp4'

def imgup(url):
	hash = hashlib.md5(bytes(url,encoding='utf-8')).hexdigest()

	img = HTMLSession().get(url).content
	name = os.path.basename(url)
	year = str(time.strftime('%Y'))
	month = str(time.strftime('%m'))
	file_path = 'C:\\xampp\\htdocs\\wp-content\\uploads\\'+year+'\\'+month+'\\'+name

	if os.path.isfile(file_path):
		name = re.sub(r'\.','_'+str(hash)+'.',name)
		with open('C:\\xampp\\htdocs\\wp-content\\uploads\\'+year+'\\'+month+'\\'+name,'wb') as f:
			f.write(img)
		return 'http://127.0.0.1/wp-content/uploads/'+year+'/'+month+'/'+name

	else:
		with open('C:\\xampp\\htdocs\\wp-content\\uploads\\'+year+'\\'+month+'\\'+name,'wb') as f:
			f.write(img)
		return 'http://127.0.0.1/wp-content/uploads/'+year+'/'+month+'/'+name
	

def fabu(url):
	html = htmldown(url)

	# 如果是图片
	post.custom_fields.append({
            'key':'type',
            'value':'img'
            })
	try:
		# 尝试寻找附件页面
		att_url = html.find('.main-shot .detail-shot a')[0].attrs['href']
	except:
		# 如果不存在附件页面，直接抓取当页图片
		att = html.find('.main-shot .detail-shot img')[0].attrs['src']
		att = imgup(img)
        post.custom_fields.append({
            'key':'att',
            'value':att
            })
        shuchu('单张图片附件',att)
	else:
		# 开始载入附件页面进行分析
		att_html = htmldown(att_url)
		try:
			# 判断附件是否有ul多张图片
			img_list = att_html.find('#attachments ul')[0].find('li')
		except:
			# 如果附件页面只有一张图
			img = att_html.find('#viewer #viewer-img img')[0].attrs['src']
			att = imgup(img)
                post.custom_fields.append({
                    'key':'att',
                    'value':att
                    })
                shuchu('单张图片附件',att)
        else:
        	# 如果附件页面存在ul有多张图片
        	att = ''
            for i in img_list:
                img = i.find('a img')[0].attrs['src']
                img = re.sub(r'\/thumbnail','',img)
                single_att = imgup(img)
                att = str(single_att)+','+att
            shuchu('多张图片附件',att)
            post.custom_fields.append({
                'key':'att',
                'value':att
                })








url = 'http://baidu.com/word.png'
on_time = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

name = os.path.basename(url)
name = on_time+'_'+name
print(name)