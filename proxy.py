import requests
import telnetlib

header_data= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'}
proxies = ['117.89.162.247:4532', '110.82.166.138:45061', '122.224.65.201:3128',
           '118.89.51.66:5000','182.148.15.88:8118', '60.191.11.237:3128',]
polar_url = 'http://d.jghttp.golangapi.com/getip?num=19&type=1&pro=350000&city=350300&yys=0&port=11&pack=21769&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='

def get_polar_ip():
    try:
        kv = header_data
        r = requests.get(polar_url, headers = kv, timeout=10)
        pageTxt = r.text
        polar_list = pageTxt.split('\r\n')
        #print(polar_list)
        return polar_list
    except Exception as e:
        print(repr(e) + url)
        return []

def test_ip(proxies):
    valid_proxies = []
    for proxy in proxies:
        str = proxy.split(':', 1)
        ip = str[0]
        port = str[1]
        try:
            telnetlib.Telnet(ip,port,timeout=2)
            valid_proxies.append(proxy)
            #print("%s %s 有效！" % (ip, port))
        except:
            #print("%s %s 无效！" % (ip, port))
            continue
    print(valid_proxies)

if __name__ == '__main__':
    get_polar_ip()
