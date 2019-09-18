"""
同步
"""
import requests
from pyquery import PyQuery as pq
import aiohttp
import time
import asyncio

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
PROXY = []
def main():
    start_time = time.time()
    for i in range(1,2):
        url = 'http://www.nimadaili.com/gaoni/{}/'.format(i)
        get_ip(url)
    end_time = time.time()
    print(end_time - start_time)

def get_ip(url):
    try:
        html = requests.get(url,headers=headers)
        if html.status_code == 200:
            doc = pq(html.text)
            tds = doc('table.fl-table tbody tr td:nth-child(1)').items()
            # print(type(tds))
            for td in tds:
                proxy = td.text()
                check_ip(proxy)
    except:
        print('getting fail')

TEST_URL = 'http://www.baidu.com'
def check_ip(proxy):
    """
    测试单个代理
    :return:
    """
    try:
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf-8')
        real_proxy = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        print('Checking:', proxy)
        # time.sleep(0.1)
        response = requests.get(TEST_URL, headers=headers, proxies=real_proxy,timeout=15)
        if response.status_code == 200:
            print('代理可以使用')
    except:
        print('代理请求失败！！！')

if __name__ == '__main__':
    main()