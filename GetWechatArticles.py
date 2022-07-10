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
    df.to_excel(fj + ".xlsx", encoding="utf-8")



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

def getArticlesInfoList(start_timestamp):
    # 需要抓取公众号的__biz参数
    biz = "MzIzMTIzNTM0MA=="
    # 个人微信号登陆后获取的uin
    uin = "NjM2NDc3NTA3"
    # 个人微信号登陆后获取的key，隔段时间更新
    # key = "4a4903f8ef6b840a5df77f6f1b04fc33527f5f6aca8acdd6f68d810233153fb57773aca2483ccae0bf87e1b10c81fd4b84a887825dae6ca053a66115e4ee992bc1bae34a61a7589e7d416038e725d22b7a618fb76af56d5b3eb055e5fa594f3f5ec4e76a31469585c6bb124422c80502a6bdd993a43fde56a0e76bde1a4d6a7e"
    # key = "4a4903f8ef6b840a506fe856213590e6a4ec017a8a09ee747bbec189cc9594bff0e17693bb93b6c2aeed95ebcbfa6e3839742bc9ee926d93088c0ad23f5474b7a02a1f99f2fccdb1238581e63fd2275051c26e508afefd23922e3d6734d8d3b442a99781b9c5736c3c67af65d26a2150656ef0b98d538f01bfbec3bc92f60f64"
    # key = "351cd3e52a9e1e14fefcaf04ca25f884e3328f1569bb14412a89fa2e9a6569dcbb8899ef22f341fd1bab4f77aef7abcfb767d7a8d11db70e54b014e236fabf593f20caa5c91871533f7c9537256728ba787bd772e6215f94358ecbad2c11f8f74e1c15679e4bd967214c33cc7c0838fc1cd86f796e0ba64a5a158f229b9940ce"
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
    fj = "迪哥讲事"
    xlsx_path = fj + ".xlsx"
    print(xlsx_path)
    if not os.path.exists(xlsx_path):
        os.mkdir(fj)
        os.mkdir(os.path.join(fj, "imgs"))
        lst = getArticlesInfoList()
        url_lst,tit_lst = demo(lst,fj)

    url_lst = get_URLList(xlsx_path)

    uh = Url2Html()
    for url,tit in url_lst:
        print(url)
        s = uh.run(url,fj, tit,mode =4)
        print(s)