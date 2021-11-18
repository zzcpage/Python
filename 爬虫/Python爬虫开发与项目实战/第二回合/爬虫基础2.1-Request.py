
"""
网络爬虫：是一种按照一定的规则，自动地抓取万维网信息的程序或者脚本。
网络爬虫可以分为：
1. 通用网络爬虫
    通过搜索引擎搜索关键词，然后从搜索引擎返回的数据中，爬取想要的数据。
2. 聚焦网络爬虫
    有针对性的爬取指定的网页链接。定向爬取相关页面。
3. 增量式网络爬虫
    也就是爬取新的数据，而对于之前爬取过的数据，不会再进行爬取。
4. 深层网络爬虫
    也就是爬取一些不能通过静态链接获取的，需要用户操作后才能访问获取的Web页面。

"""

#1. 下载网页
"""
Python对HTTP请求的支持：通过urllib2和urllib或者通过request模块。
一般通过request实现http请求。


    #发送get请求
    r = requests.get('')
    # 对于带有参数的url，可以通过建立一个map作为参数进行请求
    payload = {'keywords':'blog:qiyeboy','pageindex':1}
    r = requests.get('',params=payload) #通过map提供参数
    #发送post请求
    r = requests.post('')
    
"""
import requests
#chardet是用于检测文本编码
import chardet

"""
    Request库：
1. request.get/post 通过该方法请求页面，通常可以设置请求头headers,cookie,允许重定向allow_redirets
以及代理proxies，超时参数timeout
2. 对于响应 r = request.get() , 包含了返回的文本信息，状态编码,字符编码，cookie等信息。
"""
def requestTemp():
    r = requests.get('www.baidu.com')
    print(r.content) # 返回字节类型的数据
    print(r.text) # 返回文本形式的html
    print(r.encoding) # 返回网页编码格式
    r.encoding = 'utf-8' # 可以自定义编码格式。然后再读取网页文本数据，这样就不会乱码
    print(r.text) # 这是在utf-8编码下的文本数据
    #通过chardet进行解码
    r.encoding = chardet.detect(r.content)['encoding']

    ### 我们可以对请求头headers进行处理,即对请求设置请求头,设置Cookie
    ### 对于请求头，我们可以通过f12查看请求头格式
    user_agent = 'Mozilla/4.0'
    headers = {'User-Agent':user_agent} #设置请求头
    #自定义Cookie
    cookies = dict(name='qiye',age='10')

    r = requests.get('www.baidu.com',headers=headers,cookies=cookies)

    # 获取响应的Cookie值
    for cookie in r.cookies.keys():
        print(r.cookies.get(cookie))

    ### 获取返回状态编码，判断请求是否成功
    if r.status_code == requests.codes.ok :
        print(r.status_code)
        print(r.headers.get('content-type'))
    else:
        r.raise_for_status() #通过raise_for_status可以抛出一个异常。

    ###自动处理Cookie方法 , 通过session，每次都可以将Cookie值带上
    s = requests.Session()
    r = s.get("wwww.baidu.com",allow_redirects=True)
    datas = {'name':'qiyi','passwd':'123'}
    # 通过Session机制，可以保证每次都加上了cookie的值，进行请求
    r = s.post('wwww.baidu.com',data=datas,allow_redirects=True)
    # 通过allow_redirects可以设置是否允许重定向

    # 通过r.history可以获取到历史信息，也就是访问成功之前的所有请求跳转信息
    print(r.history)

    #设置超时参数，Timeout
    r = requests.get('www.baidu.com',timeout=2)

    #代理设置，使用代理Proxy,可以为任意请求方法通过设置proxies参数来配置单个请求
    proxies = {
        "http":"http://0.10.1.10:3128",
        "https":"http://10.10.1.10:1080",
        #"http":"http://user:pass@10.10.1.10:3128" #这是代理中身份认证的用户名和密码，来设置代理
    }
    requests.get("www.baidu.com",proxies=proxies) #设置代理ip

