import requests
import re
import bs4
import random
import time
import telnetlib
from excel import *
from proxy import *
from log import *

url = 'https://cl.2dsg.ga/thread0806.php?fid=25&search=&page='
url_root = 'https://cl.2dsg.ga/'
seed_root = 'magnet:?xt=urn:btih:'
header_data= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'}
key_word = re.compile('合集|极品|稀有|精品|最新|流出|女神|经典')
#key_word = ''
#proxies = ['117.89.162.247:4532', '110.82.166.138:45061', '122.224.65.201:3128',
          # '118.89.51.66:5000','182.148.15.88:8118', '60.191.11.237:3128',]
proxies = []
current_proxy_num = 3
max_proxy_num = 0
currentPage = 1
startPage = 2

def proxies_change(proxy_num):
    global max_proxy_num
    proxy_num  = proxy_num + 1
    if proxy_num == max_proxy_num:
        proxy_num =0
    return proxy_num

def spiderPage(url, timeout=20, encoding='GBK'):
    loginf(' ')
    global current_proxy_num
    try:
        kv = header_data
        r = requests.get(url, headers = kv, proxies ={'https':proxies[current_proxy_num]}, timeout=timeout)
        proxies_change(current_proxy_num)
        header = requests.head(url)
        r.encoding = encoding
        pageTxt = r.text
        return pageTxt
    except Exception as e:
        print(repr(e) + url)
        return ''

#url = 'http://d.jghttp.golangapi.com/getip?num=1&type=1&pro=350000&city=350300&yys=0&port=11&pack=21769&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
#s = spiderPage(url, encoding='utf-8')
#print(s)
#exit()
def filesave(str, name, encode='GBK'):
    loginf(' ')
    with open(name, 'w', encoding=encode) as fp:
        fp.write(str)
        fp.close()

def picDownload(url, path, name):
    loginf(' ')
    try:
        req = requests.get(url, headers = kv, timeout=10)
        addr = path + name
        with open(addr, 'wb', encoding='utf-8') as fp:
            fp.write(req.content)
    except Exception as e:
        print(repr(e))

def get_max_page(url):
    loginf(' ')
    txt = spiderPage(url, 30)
    if txt == '':
        return 0
    bs4Obj = bs4.BeautifulSoup(txt, 'html.parser')
    inputList = bs4Obj.findAll('input')
    maxPage = 0
    for name in inputList:
        if name.get('onblur') == None:
            continue
        s = re.search("this.value='1/(.+)'", name.get('onblur'))
        maxPage = int(s.group(1))
        break
    return maxPage

def get_parent_list(url, maxPage):   #maxPage网页组成的列表
    url_list = []
    for page in range(1, maxPage+1):
        url_list.append(url + str(page))
    return url_list

def get_child_list(url):          #网页内标题组成列表 名字+链接
    loginf(' ')
    childList = []
    txt = spiderPage(url)
    if txt == '':
        return childList
    bs4Obj = bs4.BeautifulSoup(txt, 'html.parser')
    name_list = bs4Obj.findAll('a', text=key_word)
    for name in name_list:
        if name.get("href") == None:
            continue
        tuple1 = name.get_text()
        tuple2 = url_root + name.get("href")
        childList.append((tuple1, tuple2))
    return childList

def get_seed(url):
    loginf(' ')
    seed = ''
    txt = spiderPage(url)
    if txt == '':
        return seed
    bs4Obj = bs4.BeautifulSoup(txt, 'html.parser')
    name_list = bs4Obj.findAll('div',class_='tpc_content do_not_catch')
    for name in name_list:
        seed_search =  re.search("[a-f0-9]{40}", str(name))
        if seed_search == None:
            continue
        seed_leaf = seed_search.group()
        seed = seed_root + seed_leaf
        break
    return seed

proxies = get_polar_ip()
max_proxy_num = len(proxies)
if len(proxies) == 0:
    exit()

maxPage = get_max_page(url)
parent_list = get_parent_list(url, maxPage)
for parent in parent_list:
    if(currentPage < startPage):
        currentPage = currentPage + 1
        continue
    print("########currentPage: %d ########" % currentPage)
    currentPage = currentPage + 1
    child_list = get_child_list(parent)
    #time.sleep(3)
    if child_list == []:
        continue
    for child in child_list:
        page_link = child[1]
        seed_link = get_seed(child[1])
        if seed_link == '':
            continue
        seed_name = child[0]
        seedAdd(seed_name, seed_link, page_link)

