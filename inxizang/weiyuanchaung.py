import execjs
import urllib.request
import json
import re
import os

os.environ["EXECJS_RUNTIME"] = "Node"

class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;

        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";

        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };

    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)

def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode('utf-8')
    return data

def translate_cn_to_en(content, tk):
    if len(content) > 4891:
        print("翻译的长度超过限制！！！")
        return
    content = urllib.parse.quote(content)
    url = "http://translate.google.cn/translate_a/single?client=t" \
          "&sl=zh-cn&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
          "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
          "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (tk, content)
    result = open_url(url)
    return result

def translate_en_to_cn(content,tk):
    if len(content) > 4891:
        print('长度超过限制')
        return
    content = urllib.parse.quote(content)
    url = "http://translate.google.cn/translate_a/single?client=t" \
          "&sl=en&tl=zh-cn&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
          "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
          "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (tk, content)
    result = open_url(url)
    return result

def cn_to_en(con):
    js = Py4Js()
    tk = js.getTk(con)
    res = str(translate_cn_to_en(con, tk))
    res = json.loads(str(res), encoding='utf-8')
    all_res = ''
    for i in res[0]:
        all_res = str(all_res) + str(i[0])
    all_res = re.sub('None', '', all_res)
    return all_res

def en_to_cn(con):
    js = Py4Js()
    tk = js.getTk(con)
    res = str(translate_en_to_cn(con,tk))
    res = json.loads(str(res),encoding='utf-8')
    all_res = ''
    for i in res[0]:
        all_res = str(all_res) + str(i[0])
    all_res = re.sub('None','',all_res)
    return all_res

def weiyuanchaung(con):
    print('原文：')
    print(con)
    text = str(con)
    text = str(cn_to_en(text))
    text = str(en_to_cn(text))
    print('\n')
    print('伪原创：')
    print(text)
    return text