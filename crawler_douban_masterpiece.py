#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:           wdf
# datetime:         10/02/2021 6:10 PM
# software:         Windows 10 PyCharm
# project name:     公众号【特里斯丹】分享
# file name:        crawler_douban_masterpiece.py
# description:      爬取豆瓣世界名著改变的电影
# usage:            

import urllib.request as urlrequset
from bs4 import BeautifulSoup
import xlsxwriter
import io
import os
import time


# 存储结果
result_path = "./世界名著改编电影/"
os.makedirs(result_path, exist_ok=True)
file = open(result_path + "世界名著改编电影.csv", "w", encoding='utf-8')
file.write("电影名, 作者, 上映年份, 评分, 电影简介, 豆瓣详情, 电影海报\n")

# 添加header
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}
url_world_film = "https://www.douban.com/doulist/1796317/?start={}&sort=seq&playable=0&sub_type="


# 从豆瓣详情页中，获取电影简介
def get_movie_details(detail_url):
    # detail_url = "https://movie.douban.com/subject/2017186/"
    req = urlrequset.Request(url=detail_url, headers=headers)
    html_content = urlrequset.urlopen(req).read().decode('utf-8')

    # 解析html
    soup = BeautifulSoup(html_content, 'html.parser')
    details = soup.find(class_='indent', id="link-report")
    
    # 如果被折叠了，则找出全文
    text = details.find(class_="all hidden")
    if text is not None:
        return text.text.strip().replace("\n", "").replace(f"\u3000", "")
    else:  # 如果没有被折叠，则直接返回
        return details.text.strip().replace("\n", "").replace(f"\u3000", "")


# 先通过url得到html内容
for i in range(6):
    url_visit = url_world_film.format(i*25)
    req = urlrequset.Request(url=url_visit, headers=headers)
    html_content = urlrequset.urlopen(req).read().decode('utf-8')

    # 查看html内容
    # print(html_content)

    # 解析html
    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup)  # 看起来更美观


    # 每页有25条信息（25个item标签）
    all_items_list = soup.find_all(class_ = "doulist-item")
    
    
    # 遍历每一页的结果
    for item in all_items_list:
        try:
            # 海报链接
            img_url = item.find("div", class_="post").find("img")['src'].replace("s_ratio_poster", "poster")    

            # 改编自xx小说
            res = item.find(class_="comment")
            author = res.text.strip().split("：")[1]

            # 年份
            res = item.find(class_="abstract")
            year = res.text.split("\n")[-2].strip()

            # 评分
            rating = item.find(class_='rating').text.strip()
            if "暂无评分" not in rating:
                rating = rating.split("\n")[0].split("：")[-1]

            # 电影标题、豆瓣详情链接
            res = item.find("div", class_='title').find('a')   
            title = res.text.strip()
            detail_url = res['href']

            # 电影简介
            detail = get_movie_details(detail_url=detail_url)

            # 保存海报
            img_req = urlrequset.Request(img_url, headers=headers)
            image_data = urlrequset.urlopen(img_req).read()
            with open(result_path + title + ".jpg", 'wb') as f:
                f.write(image_data)
            print(f"{title} , {author} , {year} , {rating}")
            file.write(f"{title}, {author}, {year}, {rating}, {detail}, {detail_url}, {img_url}\n")
            time.sleep(2)
        except:
            print('fail once')
file.close()   