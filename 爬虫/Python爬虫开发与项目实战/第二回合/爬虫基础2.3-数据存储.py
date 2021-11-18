import requests
import json
import csv
from bs4 import BeautifulSoup
# 定义获取网页文本代码
"""
    从以下的过程可以看出，对于爬虫爬取网页的过程，主要在于信息的提取，对于网页可能有用的数据进行搜集
"""
def getHtmlText(url,user_agent):
    headers = {'User-Agent':user_agent}
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    if r.status_code == 200 :
        return r.text
    else:
        r.raise_for_status()
        return ""
def saveJson():
    # 设置代理头
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'
    url = "http://seputu.com/"
    text = getHtmlText(url, user_agent)
    content = []
    if text != "":
        soup = BeautifulSoup(text, "html.parser", from_encoding='utf-8')
        for mulu in soup.find_all(class_='mulu'):
            h2 = mulu.find('h2')
            if h2 != None:
                list = []
                h2_title = h2.string  # 获取标题
                # 获取所有a标签中url和章节内容
                for a in mulu.find(class_='box').find_all('a'):
                    href = a.get('href')
                    box_title = a.get('title')
                    box_title = box_title.split(' ', 2)[2]
                    list.append({'href': href, 'box_title': box_title})
                content.append({'title': h2_title, 'content': list})
        with open('qiye.json', 'w+', encoding='utf-8') as fp:
            json.dump(content, fp, indent=4, ensure_ascii=False)  # indent用于格式化数据，如果为0或空就一行显示。

def saveCSV():
    # 设置代理头
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53'
    url = "http://seputu.com/"
    text = getHtmlText(url,user_agent)
    content = []
    if text != "":
        soup = BeautifulSoup(text,"html.parser",from_encoding='utf-8')
        for mulu in soup.find_all(class_='mulu'):
            h2 = mulu.find('h2')
            if h2!= None:
                h2_title = h2.string # 获取标题
                # 获取所有a标签中url和章节内容
                for a in mulu.find(class_='box').find_all('a'):
                    href = a.get('href')
                    box_title = a.get('title')
                    box_title = box_title.split(' ',2)[2]
                    content.append((box_title,href))
        header = ['title', 'href' ]
        with open('qiye.csv','w+',encoding='utf-8') as fp:
             f_csv = csv.writer(fp)
             f_csv.writerow(header)
             f_csv.writerows(content)

if __name__ == '__main__':
    saveCSV()

