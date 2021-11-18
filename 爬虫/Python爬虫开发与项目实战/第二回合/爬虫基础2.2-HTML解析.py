"""
正则表达式：
\b: 匹配单词的开始或结束
^:  匹配字符串的开始
$:  匹配字符串的结束
\w: 匹配字母，数字，下划线或汉字
\s: 匹配任意空白字符
\d: 匹配数字
. : 匹配除换行符以外的任意字符

字符串转义: 通过\进行转义
数量匹配：
*：零次或多次
+： 一次或多次
？：零次或一次
{n}: n次
{n,}: n次或更多次
{n,m} 重复n-m次

分支条件：
正则表达式通过 | 表示或的关系。
"""

"""
    这里采用BeautifulSoup(美味汁)进行文本解析
"""
from bs4 import BeautifulSoup
import requests
import re
r = requests.get("http://www.baidu.com")
r.encoding = 'utf-8'
html = r.text
# 可以直接打开，不知道解析器，一般采用lxml解析器
soup = BeautifulSoup(html,'lxml',from_encoding='utf-8')

def 获取对象属性():

    #Tag 对象
    #Tag对象就像html标签一样，直接通过soup.标签名进行对象的提取
    #要获取tag对象的属性，通过标签.name获取标签的名称 ， 并且可以设置标签的名称
    #如果需要获取标签的属性，如href和class之类的属性，则通过标签.get(属性名)

    print(soup.a) # 根据标签获取
    print(soup.a.name) #获取标签名称
    print(soup.a.get('href')) # 获取属性名称
    print(soup.a.attrs) # 获取标签中的所有属性

    # 如果要修改标签中的属性，怎么获取也同样可以怎么设置

    # BeautifulSoup用NavigableString类来包装Tag中的字符串，通过标签.string就可以获取到标签内部的文字
    print(soup.a.string)
    print(type(soup.a.string))

    #BeautifulSoup对象表示的是一个文档的全部内容。


def 遍历():
    ### 遍历操作， beautiful soup 对文档树的遍历
    """
    1. contents
    2.  children
    """
    # contents属性，可以将tag的子节点列表输出
    print(soup.head.contents)
    # children属性返回的是一个生成器。可以对Tag的子节点进行循环
    # 也就是通过children可以迭代遍历节点的所有子节点.
    for child in soup.head.children:
        print(child)
    # 如果要递归遍历所有标签的孙子结点，则通过desendants属性，对所有tag的子孙节点进行循环
    # 标签的内容也属于标签的子节点
    for child in soup.head.descendants:
        print(child)

    # 获取结点的内容

    # stirng , 如果标记唯一就返回标记的内容，而如果标记不唯一，可能返回None
    print(soup.a.string)

    # strings属性主要用于tag中包含多个字符串的情况，可以循环遍历
    for string in soup.strings:
        print(string)

    # stripped_strings 可以去掉输出字符串包含的空格或空行
    for string in soup.stripped_strings:
        print(string)

    # 获取父节点，通过parent属性
    print(soup.a.parent)

    # 获取节点的所有父辈节点，通过parents属性
    for parent in soup.a.parents:
        if parent is None:
            print(parent)
        else:
            print(parent.name)

    # 获取节点的兄弟节点,空白或换行也可也被视作一个节点
    # next_sibling获取下一个兄弟节点
    print(soup.a.next_sibling)
    # previous_sibling获取上一个兄弟节点
    print(soup.a.previous_sibling)
    # 通过next_siblings或者previous_siblings可以对当前兄弟节点迭代输出
    for sibling in soup.a.next_siblings:
        print(sibling)

    # 获取节点的前后节点。前后节点是不区分层次结构的前后关系，如<div><a><div>,div的后一个节点就是a
    # next_element,previous_element,
    print(soup.a)
    print(soup.a.next_element)

    # 如果想遍历所有前后节点，通过next_elements和previous_elements进行遍历
    for element in soup.a.next_elements:
        print(element)

# 搜索文档树，搜索指定的内容
def 搜索():

    # find_all()方法，搜索当前tag的所有tag子节点，判断是否满足搜索条件
    # find_add(name,attrs,recursive,txext,**kwargs)
    # name参数可以查找所有名字为name的标记,返回列表.一般用这个来找指定的标签
    # name参数可以是单独的字符，也可以是字符列表。
    # 可以自定义过滤器，用于匹配指定规则的标签
    print(soup.find_all('a'))
    print(soup.find_all(['a','b']))
    def hasClass_Id(tag):
        return tag.has_attr('class') and tag.has_attr('id')
    print(soup.find_all(hasClass_Id)) # 寻找满足匹配规则的标签
    # 多条件过滤标签
    # 可以在find_all()中根据属性搜索指定的标签，并且可以将正则表达式作为搜索条件
    print(soup.find_all('a',href=re.compile('elsie'),id='12',class_='sister'))

    #如果要限制搜索数目，则通过limit参数进行限制
    print(soup.find_all('a',limit=5))

    # 限制只搜索直接节点，而不搜索子孙节点，设置recursive = False
    print(soup.find_all('a',limit=5),recursive=False)

    # CSS选择器
    # 通过元素的CSS属性定位元素的位置
    # 根据name属性通过.class值 , 根据id属性通过#id值
    # 返回类型为list
    #找到所有a标签
    soup.select('a')
    #找到a标签，id为1
    soup.select('a#1')
    #根据name查询
    soup.select('.classs')
    #通过判断是否存在某个属性进行查找
    soup.select('a[href]')
    #通过属性值查找 ， test可以是待查找的字符串，可以通过正则表达式查询
    #href^= "" , href$= , href*= , 进行正则判断。
    soup.select('a[href="test"]')