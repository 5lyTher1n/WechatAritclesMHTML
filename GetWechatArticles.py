import os
import re
import time

import requests
from bs4 import BeautifulSoup as bs
from GetWecharArticlesHTML import Url2Html
import json
import os
import random
import time
from pprint import pprint

import pandas as pd
from wechatarticles import ArticlesInfo
from wechatarticles.utils import get_history_urls, verify_url

# 快速获取大量文章urls（利用历史文章获取链接）


def save_xlsx(fj, lst):
    df = pd.DataFrame(lst, columns=["url", "title", "date"])
    # df.to_excel(fj + ".xlsx", encoding="utf-8")
    df.to_excel(fj + ".xlsx")



def demo(lst,fj):
    flag = 0
    item_lst = []
    for i, line in enumerate(lst, 0):
        print("index:", i)
        # item = json.loads('{' + line + '}', strict=False)
        item = line
        print(item)
        timestamp = item["comm_msg_info"]["datetime"]
        ymd = time.localtime(timestamp)
        date = "{}-{}-{}".format(ymd.tm_year, ymd.tm_mon, ymd.tm_mday)

        infos = item["app_msg_ext_info"]
        url_title_lst = [[infos["content_url"], infos["title"]]]
        if "multi_app_msg_item_list" in infos.keys():
            url_title_lst += [
                [info["content_url"], info["title"]]
                for info in infos["multi_app_msg_item_list"]
            ]

        for url, title in url_title_lst:
            try:
                if not verify_url(url):
                    continue
                # 获取文章阅读数在看点赞数
                # read_num, like_num, old_like_num = ai.read_like_nums(url)
                # print(read_num, like_num)
                # item_lst.append([url, title, date, read_num, like_num])
                item_lst.append([url, title, date])
                # time.sleep(random.randint(5, 10))
            except Exception as e:
                print(e)
                flag = 1
                break
            finally:
                pass
                # save_xlsx(fj, item_lst)

        if flag == 1:
            break

    save_xlsx(fj, item_lst)
    return [[u[0],u[1]] for u in item_lst]

def getArticlesInfoList(start_timestamp=0):
    # 需要抓取公众号的__biz参数
    # biz = "MzIzMTIzNTM0MA=="
    # guimaizi
    biz = "Mzg4MzY3MTgyMw=="
    # 个人微信号登陆后获取的uin
    uin = "NjM2NDc3NTA3"
    # 个人微信号登陆后获取的key，隔段时间更新
    key = ""
    evelst = get_history_urls(
        biz, uin, key, lst=[], start_timestamp=start_timestamp, start_count=0, end_count=200
    )

    print("抓取到的文章链接")
    lst = []
    for l in evelst:
        lst += l
    print(lst, len(lst))
    return lst

def get_URLList(xlsx_path):
    df_url = pd.read_excel(xlsx_path)
    url_lst = df_url["url"]
    tit_lst = df_url["title"]
    ret_lst = []
    idx = 0
    for u in url_lst:
        ret_lst.append([u, tit_lst[idx]])
        idx += 1
    # print(url_lst)
    return ret_lst

if __name__ == "__main__":
    # 公众号名称，用来建立文件夹、保存更新URL xlsx等。
    fj = "guimaizi"
    xlsx_path = fj + ".xlsx"
    print(xlsx_path)
    if not os.path.exists(xlsx_path):
        os.mkdir(fj)
        # os.mkdir(os.path.join(fj, "imgs"))
        lst = getArticlesInfoList()
        info_list = demo(lst,fj)

    url_lst = get_URLList(xlsx_path)
    for url in url_lst:
        print(url)
    # uh = Url2Html()
    # for url,tit in url_lst:
    #     print(url)
    #     s = uh.run(url,fj, tit,mode =4)
    #     print(s)