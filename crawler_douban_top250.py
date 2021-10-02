#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:           wdf
# datetime:         10/02/2021 5:23 PM
# software:         Windows 10 PyCharm
# project name:     公众号【特里斯丹】分享
# file name:        crawler_douban_top250.py
# description:      爬取豆瓣电影top250榜单
# usage:            


import urllib.request as urlrequset
from bs4 import BeautifulSoup
import xlsxwriter
import io
import os
import time

top250_url = "https://movie.douban.com/top250?start={}&filter="

# 添加header
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}

# 存储结果
result_path = "./豆瓣电影TOP250/"
os.makedirs(result_path, exist_ok=True)
file = open(result_path + "豆瓣电影TOP250.csv", "w")
file.write("电影名, 豆瓣详情, 电影海报\n")

# 一共250条， 每页25条
for i in range(10):
    # 先通过url得到html内容
    url_visit = top250_url.format(i*25)
    req = urlrequset.Request(url=url_visit, headers=headers)
    html_content = urlrequset.urlopen(req).read().decode('utf-8')

    # 查看html内容
    # print(html_content)

    # 解析html
    soup = BeautifulSoup(html_content, 'html.parser')
    # print(soup)  # 看起来更美观
    
    # 每页有25条信息（25个item标签）
    all_items_list = soup.find_all(class_ = "item")
    for item in all_items_list:
        # 每个item下面只有一个pic标签
        pic_div = item.find(class_='pic')
        # 每个pic标签包含 电影详情链接、电影海报图片
        item_href = pic_div.find('a')['href']
        item_name = pic_div.find('img')
        item_name_title = item_name['alt']
        item_name_img = item_name['src'].replace('jpg', 'webp').replace("s_ratio_poster", "poster")

        # 打印信息
        print("{}, {}, {}".format(item_name_title, item_href, item_name_img))
        file.write("{}, {}, {}\n".format(item_name_title, item_href, item_name_img))
        # 保存海报
        img_req = urlrequset.Request(item_name_img, headers=headers)
        image_data = urlrequset.urlopen(img_req).read()
        with open(result_path + item_name_title + ".jpg", 'wb') as f:
            f.write(image_data)
file.close()