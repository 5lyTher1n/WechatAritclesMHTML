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



def demo(lst):
    # 抓取示例，供参考，不保证有效
    fj = "迪哥讲事"
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
                save_xlsx(fj, item_lst)

        if flag == 1:
            break

    save_xlsx(fj, item_lst)


if __name__ == "__main__":
    # 需要抓取公众号的__biz参数
    biz = "MzIzMTIzNTM0MA=="
    # 个人微信号登陆后获取的uin
    uin = "NjM2NDc3NTA3"
    # 个人微信号登陆后获取的key，隔段时间更新
    # key = "4a4903f8ef6b840a5df77f6f1b04fc33527f5f6aca8acdd6f68d810233153fb57773aca2483ccae0bf87e1b10c81fd4b84a887825dae6ca053a66115e4ee992bc1bae34a61a7589e7d416038e725d22b7a618fb76af56d5b3eb055e5fa594f3f5ec4e76a31469585c6bb124422c80502a6bdd993a43fde56a0e76bde1a4d6a7e"
    key = "4a4903f8ef6b840a506fe856213590e6a4ec017a8a09ee747bbec189cc9594bff0e17693bb93b6c2aeed95ebcbfa6e3839742bc9ee926d93088c0ad23f5474b7a02a1f99f2fccdb1238581e63fd2275051c26e508afefd23922e3d6734d8d3b442a99781b9c5736c3c67af65d26a2150656ef0b98d538f01bfbec3bc92f60f64"
    evelst = get_history_urls(
        biz, uin, key, lst=[], start_timestamp=0, start_count=0, end_count=200
    )

    print("抓取到的文章链接")
    lst = []
    for l in evelst:
        lst += l
    print(lst,len(lst))
    demo(lst)
    # for l in lst:
    #     print(l)
    #     demo(l)


    # # 个人微信号登陆后获取的token
    # appmsg_token = ""
    # # 个人微信号登陆后获取的cookie
    # cookie = ""
    # # 获取点赞数、阅读数、评论信息
    # ai = ArticlesInfo(appmsg_token, cookie)
    #
    # # url：微信文章链接. lst[0]["app_msg_ext_info"]["content_url"]
    # read_num, like_num, old_like_num = ai.read_like_nums(url)
    # item = ai.comments(url)
    # print("阅读：{}; 在看: {}; 点赞: {}".format(read_num, like_num, old_like_num))
    # print("评论信息")
    # pprint(item)