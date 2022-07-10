from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from GetWechatArticles import getArticlesInfoList, demo
from wechatarticles.utils import get_history_urls, verify_url
from mongodb import get_last_record,add_record
import time
import os
import random
import re
import pandas as pd

def get_URLList(xlsx_path):
    df_url = pd.read_excel(xlsx_path)
    url_lst = df_url["url"]
    tit_lst = df_url["title"]
    date_list = df_url['date']
    ret_lst = []
    idx = 0
    for u in url_lst:
        ret_lst.append([u, tit_lst[idx],date_list[idx]])
        idx += 1
    # print(url_lst)
    return ret_lst



def replace_name(title):
        """
        对进行标题替换，确保标题符合windows的命名规则
        Parameters
        ----------
        title: str
            文章标题
        Returns
        ----------
        str: 替换后的文章标题
        """
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        title = re.sub(rstr, "", title).replace("|", "").replace("\n", "")
        return title

def getMHTML(url, filename):
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(url)
    js_hight = "return document.body.scrollHeight"
    hight = int(driver.execute_script(js_hight))

    for i in range(10000):
        random_num = random.randint(3,5)
        time.sleep(random_num)
        idx = i * 500
        # target = driver.find_element_by_class_name("function_hd js_related_title")
        # target = driver.find_element(By.CLASS_NAME,'function_bd')
        print(i*500, random_num, hight)
        js = "document.documentElement.scrollTop=%d" % idx
        if(hight < idx):
            break
        driver.execute_script(js)


    res = driver.execute_cdp_cmd('Page.captureSnapshot', {})


    # 2. 写入文件
    with open(filename, 'w', newline= '') as f:
        f.write(res['data'])

    driver.quit()

def get_start_timestamp(date):
    struct_time = time.strptime(date, '%Y-%m-%d')
    start_timestamp = int(time.mktime(struct_time)) - 1;
    return  start_timestamp

def processLst(lst):
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
                item_lst.append([url, title, date])

            except Exception as e:
                print(e)
                flag = 1
                break
            finally:
                pass
                # save_xlsx(fj, item_lst)

        if flag == 1:
            break

    # return [[u[0], u[1]] for u in item_lst]
    return item_lst


if __name__ == "__main__":

    # 公众号名称，用来建立文件夹、保存更新URL xlsx等。
    gzh_name = "迪哥讲事"
    last_date, last_record_url, last_record_title = get_last_record(gzh_name)

    start_timestamp = get_start_timestamp(last_date)

    lst = getArticlesInfoList(start_timestamp)
    info_list = processLst(lst)

    print(info_list)

    for eve in info_list:
        cur_url = eve[0]
        cur_tit = replace_name(eve[1])
        # tit = eve[1]
        cur_date = eve[2]
        if cur_date < last_date:
            break
        if cur_url not in last_record_url or cur_tit not in last_record_title:
            print(" === ", cur_url, cur_tit, cur_date)
            add_record(gzh_name, [cur_url, cur_tit, cur_date])

            filename = "[{}]-{}-{}".format(gzh_name, cur_date, cur_tit)
            filename = "./mhtml/{}/".format(gzh_name) + filename + ".mhtml"
            if os.path.exists(filename):
                continue
            getMHTML(cur_url, filename)
            time.sleep(random.randint(1,3))


