from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
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

if __name__ == "__main__":

    # 公众号名称，用来建立文件夹、保存更新URL xlsx等。
    fj = "迪哥讲事"
    xlsx_path = fj + ".xlsx"
    print(xlsx_path)
    # if not os.path.exists(xlsx_path):
    #     os.mkdir(fj)
    #     os.mkdir(os.path.join(fj, "imgs"))
    #     lst = getArticlesInfoList()
    #     url_lst,tit_lst = demo(lst,fj)

    url_lst = get_URLList(xlsx_path)

    # uh = Url2Html()
    for url,tit,date in url_lst:
        tit = replace_name(tit)
        print(len(url))
        # filename = "[{}]-{}-{}".format(fj, date, tit)
        # filename = "./mhtml/" + filename  + ".mhtml"
        # if os.path.exists(filename):
        #     continue
        # getMHTML(url, filename)
        # time.sleep(random.randint(1,3))


