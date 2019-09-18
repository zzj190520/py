"""
异步协程
获取http://www.nimadaili.com/ 泥马IP代理
"""
import requests
from pyquery import PyQuery as pq
import aiohttp
import time
import asyncio
count = 0
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
PROXY = []

def get_ip(url):
    try:
        html = requests.get(url,headers=headers)
        if html.status_code == 200:
            doc = pq(html.text)
            tds = doc('table.fl-table tbody tr td:nth-child(1)').items()
            # print(type(tds))
            for td in tds:
                PROXY.append(td.text())
    except:
        print('getting fail')


TEST_URL = 'https://m.weibo.cn/api/statuses/repostTimeline?id=4409206209667284&page=1'
PROXY_STEP = 100
def run():
    print("异步测试器开始运行")
    try:
        loop = asyncio.get_event_loop()
        for i in range(0, len(PROXY), PROXY_STEP):
            test_proxy = PROXY[i:i + PROXY_STEP]
            tasks = [check_ip(proxy) for proxy in test_proxy]
            loop.run_until_complete(asyncio.wait(tasks))
            # time.sleep(5)
    except:
        print('异步测试发生错误！！！')

async def check_ip(proxy):
    """
    测试单个代理
    :return:
    """
    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        try:
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')
            real_proxy = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
            print('Checking:', proxy)
            # time.sleep(0.1)
            response = requests.get(TEST_URL, headers=headers, proxies=real_proxy,timeout=6)
            if response.status_code == 200:
                print('代理可以使用')
                save_ip(proxy)
        except:
            print('代理请求失败！！！')

def save_ip(proxy):
    try:
        with open('E:\code\Spyder_document\prox\proxy_nima.txt', 'a', encoding='utf-8') as f:
            f.write(proxy + '\n')
    except:
        print("存储proxy失败")

def main():
    start_time = time.time()
    for i in range(1,20):
        url = 'http://www.nimadaili.com/gaoni/{}/'.format(i)
        get_ip(url)
    run()
    end_time = time.time()
    print(end_time - start_time)

if __name__ == '__main__':
    main()