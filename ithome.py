# coding=utf-8
import requests
import urllib.request
import io
import sys

import pymysql

from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


# 打开数据库连接并获取cursor
def connectDatabase():
    db = pymysql.connect(host='47.99.54.53', port=3306, user='root', passwd='Dan05174530~', db='ithouse',
                         charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    # cursor = db.cursor()
    return db


# 创建数据库
def createDatabase():
    db = connectDatabase()
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS newslist")

    # 使用预处理语句创建表
    sql = """CREATE TABLE newslist (
             title  CHAR(200),
             detail_href CHAR(200),
             pic CHAR(100),
             time CHAR(100),
             comment_num CHAR(100))"""

    cursor.execute(sql)



# 插入数据到数据库表
def insertData2Newslist(dataList):
    db = connectDatabase()
    cursor = db.cursor()

    #先删除表内容
    sql = "DELETE FROM newslist"

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

    #SQL 插入语句
    sql = "INSERT INTO newslist(title,detail_href,pic,time,comment_num) VALUES (%s,%s,%s,%s,%s)"

    try:
        # 执行sql语句
        # cursor.execute(sql)
        cursor.executemany(sql, dataList)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        info = sys.exc_info()
        print(info[0], ":", info[1])

    # 关闭数据库连接
    db.close()



def getithome():
    url = "https://www.ithome.com/"

    html = urllib.request.urlopen(url).read()
    htmlUtf8 = html.decode("utf-8", "ignore")

    soup = BeautifulSoup(htmlUtf8, 'lxml')
    # print(soup.prettify())

    # news_titles = soup.select(".nlquan a")
    # fp = open("C:/Users/Danmo/Desktop/ssss.txt", "w+", encoding="utf-8")
    #
    # for kk in news_titles:
    #     mm = kk.get_text()
    #     print(mm)
    #     fp.write(mm)
    #     fp.write("\n")

    list = []
    content_title = soup.select(".new")
    for content_titleItem in content_title:
        time = content_titleItem.select(".date")[0].get_text()
        content = content_titleItem.select(".title > a")[0].get_text()
        href = content_titleItem.select(".title > a")[0].get('href')
        list.append((content, href, "www.baidu.com/pic", time, 199))

    #插入到数据库
    insertData2Newslist(list)

    # for gg in content_title:
    #     title = gg.get_text()
    #     detail_href = gg.get('href')
    #     print(detail_href)

    # fp.write(href)
    # fp.write("\n")
    # print(mm)
    # fp.write(mm)
    # fp.write("\n")
    # fp.close()


def main():
    # getithome()
    # createDatabase()
    # 获取标题列表
    getithome()

#  460043274408481
main()
