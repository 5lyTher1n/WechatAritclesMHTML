from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import pyautogui
from selenium.webdriver.chrome.service import Service

# s = Service("D:\WebDriver\chromedriver_win_103\chromedriver.exe")
# driver = webdriver.Chrome(executable_path="D:\WebDriver\chromedriver_win_103\chromedriver.exe")


# options = webdriver.ChromeOptions()
# options.add_argument('--save-page-as-mhtml')
driver = webdriver.Chrome()
# driver.maximize_window()
# url = "http://mp.weixin.qq.com/s?__biz=MzIzMTIzNTM0MA==&amp;mid=2247485798&amp;idx=1&amp;sn=a98c8ac673ba271f7d5a489bedcb606c&amp;chksm=e8a60305dfd18a136ff27f28ada8f714b63fd52ecc5bc07e9d19594698263ec757503d7f2c35&amp;scene=27#wechat_redirect"
# url = "https://mp.weixin.qq.com/s/wOlB6vkgAM5fAb4TvziGpA"
# url = "https://mp.weixin.qq.com/s?__biz=MzIzMTIzNTM0MA==&amp;mid=2247485605&amp;idx=1&amp;sn=082cb4eee3dc245710a02a6d00c1dbf5&amp;chksm=e8a602c6dfd18bd0820086a952721fdfbf74cf900de23625e4c7bb7bb3ab4f848c1bd3499c29&amp;scene=27#wechat_redirect"

url = "https://www.cnblogs.com/sui776265233/p/9714028.html"

driver.get(url)
js_hight = "return document.body.scrollHeight"
hight = int(driver.execute_script(js_hight))
# driver.execute_script('window.scrollTo(0, %s)' % hight)
# time.sleep(3)
# print(hight)
for i in range(10000):
    random_num = random.randint(2,4)
    time.sleep(random_num)
    idx = i * 500
    # target = driver.find_element_by_class_name("function_hd js_related_title")
    # target = driver.find_element(By.CLASS_NAME,'function_bd')
    print(i*500, random_num, hight)
    js = "document.documentElement.scrollTop=%d" % idx
    if(hight < idx):
        break
    driver.execute_script(js)

# WebDriverWait(driver, 60).until(visibility_of_element_located(By.CLASS_NAME,'function_bd'))
# time.sleep(10)
# FILE_NAME = ''
# pyautogui.hotkey('ctrl', 's')
# time.sleep(1)
# if FILE_NAME != '':
#     pyautogui.typewrite(FILE_NAME)
# pyautogui.hotkey('enter')
# print(FILE_NAME)
# driver.quit()
# 1. 执行 Chome 开发工具命令，得到mhtml内容
res = driver.execute_cdp_cmd('Page.captureSnapshot', {})

# 2. 写入文件
with open('zzzqqq.mhtml', 'w', newline= '') as f:
    f.write(res['data'])

driver.quit()
# %%time
# # 通过判断已无更多的style,来判断是否到最底部，最终执行到最底部
# no_more_msg_style = 'display: none;'
# while True:
#     wait.until(EC.presence_of_element_located((By.XPATH,'//span[@class="tips js_no_more_msg" and text()="已无更多"]')))
#     no_more= browser.find_element_by_xpath('//span[@class="tips js_no_more_msg" and text()="已无更多"]')
#     now_style = no_more.get_attribute('style')
#     if str(now_style).find(no_more_msg_style) == -1:
#         # 说明已经加载完了
#         break
#     else:
#         # 停顿一会，等待浏览器加载
#         time.sleep(5)
#         # 通过JS，执行到最底部
#         browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')