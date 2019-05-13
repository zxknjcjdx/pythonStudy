import requests
import pandas as pd
from lxml import etree
import os

def getHtml(url):
    try:
        html = requests.get(url,timeout=30)
        html.encoding = html.apparent_encoding
        if html.status_code ==200:
            print("获取数据成功")
    except:
        print("获取数据失败")
    return html.text

def parse_html(html):
    html = etree.HTML(html)
    info = html.xpath("//div[@class='article']/div/p/span/text()")
    return info

if __name__ == '__main__':
    data = pd.read_csv("F:/pachong/电影具体内容/1.csv", encoding="GBK")
    data = data.iloc[:, 1:2]
    data.columns = ['name']  # 给这一列加一个名字为name的索引
    data["year"] = data["name"].map(lambda x: x[-5:-1])  # 给data加一列 这列的索引为year，然后取其年份 形成新的一列
    data["name"] = data["name"].map(lambda x: x[:-6])  # 去掉name这一列的（年份）
    count = data.describe().loc["count"]["name"]
    for i in range(1681):
        try:
            name = data.iloc[i]["name"]
            year = data.iloc[i]["year"]
            url = "https://www.imdb.com/find?ref_=nv_sr_fn&q={}+({})&s=all".format(name,year)
            html = getHtml(url)
            html = etree.HTML(html)
            u = html.xpath("//td[@class='result_text']/a/@href")
            url = "https://www.imdb.com" + u[0]
            html = getHtml(url)
            movieInfo = parse_html(html)
            os.chdir("F:/pachong/电影具体内容")
            with open("编号{}电影信息.txt".format(i+1),'w') as f:
                f.write(str(movieInfo))
        except:
            continue

