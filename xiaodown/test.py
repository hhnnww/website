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

year = str(time.strftime('%Y'))
month = str(time.strftime('%m'))

if os.path.exists('C:\\xampp\\htdocs\\wp-content\\uploads\\'+year) == False:
	os.mkdir('C:\\xampp\\htdocs\\wp-content\\uploads\\'+year)

if os.path.exists('C:\\xampp\\htdocs\\wp-content\\uploads\\'+year+'\\'+month) == False:
	os.mkdir('C:\\xampp\\htdocs\\wp-content\\uploads\\'+year+'\\'+month)