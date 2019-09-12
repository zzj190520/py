"""
爬取王思聪m站微博
"""
import requests
import json

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
    }

def get_useinfor(ID, real_proxy):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='+ID
    # print(url)
    res = requests.get(url,headers=headers,proxies=real_proxy,timeout=6)
    data = res.json()
    content = data.get('data')
    userInfo = content.get('userInfo')
    name = userInfo.get('screen_name')
    verified_reason = '微博认证：'+userInfo.get('verified_reason')
    description = '个性签名：'+userInfo.get('description')
    head_photo = '微博头像：'+userInfo.get('cover_image_phone')
    follow_count = '关注：'+str(userInfo.get('follow_count'))
    followers_count = '粉丝：'+str(userInfo.get('followers_count'))
    for item in content.get('tabsInfo').get('tabs'):
        if item.get('tab_type') == 'weibo':
            containerid = item.get('containerid')
    with open('wsc.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join([name,verified_reason,description,head_photo,follow_count,followers_count]))
        f.write('\n')
    return containerid

def get_content(ID, containerid,real_proxy):
    global count
    global page
    try:
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='+ ID + '&containerid='+ containerid + '&page=' + str(page)
        resp = requests.get(url=weibo_url, headers=headers,proxies=real_proxy,timeout=6)
        json = resp.json()
        data = json.get('data')
        print(weibo_url)
        for card in data.get('cards'):
            mblog = card.get('mblog')
            print('正在爬取第',count,'条微博')
            weibo_num = '第' + str(count) + '条微博'
            title = '微博内容：' + mblog.get('text')
            created_at = '时间：' + mblog.get('created_at')
            reposts_count = '转发：' + str(mblog.get('reposts_count'))
            comments_count = '评论：' + str(mblog.get('comments_count'))
            attitudes_count = '点赞：' + str(mblog.get('attitudes_count'))
            with open('wsc.txt','a',encoding='utf-8') as f:
                f.write('\n'.join([weibo_num, title, created_at, reposts_count, comments_count, attitudes_count]))
                f.write('\n')
            count = count + 1
        page = page + 1
        get_content(ID, containerid, real_proxy)
    except:
        pass

count = 1
page = 1
def main():
    ID = '1826792401'  # 王思聪
    with open('proxy.json', 'r') as f:
        proxy_str = f.read()
        real_proxies = json.loads(proxy_str)
    print('正在获取用户信息')
    i = 0
    while i<len(real_proxies):
    # for i in range(len(real_proxies)):
        real_proxy = {
            'http': 'http://' + real_proxies[i],
            'https': 'https://' + real_proxies[i]
        }
        print('正在使用第',i,'个代理：',real_proxy)
        try:
            containerid = get_useinfor(ID, real_proxy)
            if containerid == '1076031826792401':
                break
        except:
            pass
        if i == (len(real_proxies)-1):
            i = 0
        else:
            i = i + 1

    print('正在爬取微博信息')
    i=0
    while i<len(real_proxies):
    # for i in range(len(real_proxies)):
        real_proxy = {
            'http': 'http://' + real_proxies[i],
            'https': 'https://' + real_proxies[i]
        }
        print('正在使用第', i, '个代理：', real_proxy)
        get_content(ID, containerid, real_proxy)
        if i == (len(real_proxies) - 1):
            i = 0
        else:
            i = i+1

if __name__ == '__main__':
    main()