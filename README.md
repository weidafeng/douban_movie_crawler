# 豆瓣电影爬虫

爬取豆瓣电影，保存`电影名`, `作者`, `上映年份`, `评分`, `电影简介`，`豆瓣详情链接`, `电影海报` 等信息。

其中文本信息以`csv`格式存储， 电影海报图片以`jpg` 格式存储。



## 1. 爬取豆瓣电影TOP250榜单

豆瓣链接：https://movie.douban.com/top250

这个程序很基础，网上也有很多示例教程，很好上手，主要用到两个常用库

```python
import urllib.request as urlrequset
from bs4 import BeautifulSoup
```

**通用的思路：**

1. 访问url，得到整页的html内容(`urllib.request`)
2. 从html中提取需要的信息(`BeautifulSoup`)

**代码也很简单：**

完整代码请参见 [crawler_douban_top250.py](./crawler_douban_top250.py)

```python
# 先通过url得到html内容
url_visit = "https://movie.douban.com/top250"
req = urlrequset.Request(url=url_visit, headers=headers)
html_content = urlrequset.urlopen(req).read().decode('utf-8')

# 查看html内容
# print(html_content)

# 解析html
soup = BeautifulSoup(html_content, 'html.parser')
# print(soup)  # 看起来更美观

# 每页有25条信息（25个item标签）
all_items_list = soup.find_all(class_="item")
for item in all_items_list:
    # 每个item下面只有一个pic标签
    pic_div = item.find(class_='pic')
    # 每个pic标签包含 电影详情链接、电影海报图片
    item_href = pic_div.find('a')['href']
    item_name = pic_div.find('img')
    item_name_title = item_name['alt']
    item_name_img = item_name['src'].replace('jpg', 'webp').replace("s_ratio_poster", "poster")  # 转换成原图链接

    # 打印信息
    print("{}, {}, {}".format(item_name_title, item_href, item_name_img))
```



## 2. 爬取豆瓣世界名著改编电影列表

豆瓣链接： https://www.douban.com/doulist/1796317/

**思路：**

1. 遍历每页，其中每页包含25条记录
2. 遍历每条记录，得到`电影名`, `作者`, `上映年份`, `评分`, `豆瓣详情链接`, `电影海报` 等信息
3. 根据`豆瓣详情链接`，得到`电影简介` 
4. 保存结果

**关键代码：**

完整代码请参见 [crawler_douban_masterpiece.py](./crawler_douban_masterpiece.py)

```python
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
```

