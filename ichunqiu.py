import requests,schedule,time,json
from lxml import etree

def get():
    url = 'https://bbs.ichunqiu.com/home.php?mod=space&uid=588931&do=thread&view=me&from=space'#填自己的文章链接。当然你想监控别人也可以
    r = requests.get(url, headers=headers, timeout=1).content.decode('utf-8')
    soup = etree.HTML(r)
    hf = soup.xpath('//td[@class="num"]/a[@target="_blank"]/text()')
    yd = soup.xpath('//td[@class="num"]/em/text()')
    bt = soup.xpath('//th/a[@target="_blank"]/text()')
    file = open("sj.txt", 'w+').close()
    for iii,i, ii in zip(bt,hf, yd):
        a = iii+'的评论量:'+i +'查看量:'+ ii
        file = open("sj.txt", "a+", encoding='utf-8')
        file.write(a + "\n")
        file.close()
def post():
    localtime = time.asctime(time.localtime(time.time()))
    url_3 = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=填AgentId&corpsecret=填Secret"
    r = requests.get(url_3, headers=headers, timeout=1).content.decode('utf-8')
    r = json.loads(r)  # 将json格式数据转换为字典
    token = r["access_token"]
    url_2 = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token
    f = open('sj.txt','r',encoding='utf-8')
    a=f.read()
    data={
   "touser" : "@all",
   "toparty" : "@all",
   "totag" : "@all",
   "msgtype" : "textcard",
   "agentid" : '填自己机器人id',
   "textcard" : {
            "title" : "i春秋文章数据",
            "description" : a,
            "url" : "URL",
                        "btntxt":"更多"
   },
   "enable_id_trans": 0,
   "enable_duplicate_check": 0,
   "duplicate_check_interval": 1800
}
    send = (bytes(json.dumps(data), 'utf-8'))
    r = requests.post(url=url_2, data=send, headers=headers).text
    print("----------------------------")
    print('现在是'+localtime)
    print(r)
    print("----------------------------")

if __name__ == '__main__':
    print("""
      _  __          _  __
     | |/,'_   _    | |/,'() _
     | ,','o| / \/7 /  / /7,'o|
    /_/  |_,7/_n_/,'_n_\// |_,7
                      QQ:210246020         
                              """)
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
               'cookie': 'aUZ1_2132_saltkey=;  ci_session=; chkphone=; Hm_lvt_2d0601bd28de7d49818249cf35d95943=; aUZ1_2132_auth=; '}
#cookie我已找好了。你们添加下就好了。经过测试。在自己服务器里一边登入论坛，一边挂脚本比较稳定。如果关了浏览器的话，cookie会过期

    schedule.every(45).minutes.do(get)
    schedule.every(45).minutes.do(post)
    get()
    post()
    while True:
       schedule.run_pending()
       time.sleep(1)
