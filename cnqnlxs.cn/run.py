from requests_html import HTMLSession

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc import WordPressTerm
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

import re
import time

import cn_sql
import cn_time

def htmldown(url):
	# proxies = {
	# 	"http":"http://127.0.0.1:1080"
	# }
	html = HTMLSession().get(url).html
	return html

def page_list():
	page_list = []
	x = 2
	while (x<=20):
		page_list.append('http://sexinsex.net/bbs/forum-110-'+str(x)+'.html')
		x = x + 1
	return page_list

def single_list():
	single_list = []
	for url in page_list():
		html = htmldown(url)
		link_list = html.find('div.mainbox')[0].find('table#forum_110')[1].find('tbody')
		for i in link_list:
			try:
				link = i.find('span.threadpages a')[0].attrs['href']
				link = 'http://sexinsex.net/bbs/'+str(link)
				single_list.append(link)
			except:
				pass
	return single_list

def fabu(url):
	wp = Client('http://cnqnlxs.cn/xmlrpc.php','admin','12qwaszx')
	post = WordPressPost()
	post.post_status = 'publish'

	print(cn_time.thetime()+str(url))
	html = htmldown(url)

	try:
		title = html.find('.mainbox h1')[0].text
		title = re.sub(r'\[.*?\]','',title)
		title = re.sub(r'(作者.*)','',title)
		title = re.sub(r'(\d)','',title)
		title = re.sub(r'(-|－)','',title)
		title = re.sub(r'(\s)','',title)
		title = re.sub(r"\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*()<>+'?@|:~{}#]+|[—！\\\，。=？、：“”‘’￥……（）《》【】]","",title)
		print(cn_time.thetime()+str(title))

		post.title = title
	except:
		print('标题错误，返回')
		return

	try:
		content = html.find('div.t_msgfont .t_msgfont')[0].text
		content = re.sub(r'(\n\n)','++',content)
		content = re.sub(r'\n','',content)
		content = re.sub(r'\+\+','\n\n',content)
		# print(content)

		post.content = content
	except:
		print('内容错误，返回')
		return

	post.id = wp.call(NewPost(post))
	print(cn_time.thetime()+'http://cnqnlxs.cn/?p='+str(post.id))
	print(cn_time.thetime()+'发布成功')

def run():
	for url in single_list():
		if str(cn_sql.sql_chaxun(url)) == 'bucunzai':
			print(cn_time.thetime()+'发现新文章开始采集')
			fabu(url)
			cn_sql.sql_charu(url)
			print(cn_time.thetime()+'url插入到数据库去重')
		else:
			print(cn_time.thetime()+'文章存在，跳过~~~')
			print('\n')

x = 1
while (x < 2):
	run()
	time.sleep(3600)