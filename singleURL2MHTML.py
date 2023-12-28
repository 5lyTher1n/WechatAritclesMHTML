# 这是一个测试文件，或者用来下载某一个页面的mhtml

from Url2MHtml import getMHTML
import os

if __name__ == "__main__":

    # 公众号名称，用来建立文件夹、保存更新URL xlsx等。
    gzh_name = "卓文见识"
    cur_tit = "越权漏洞（e.g. IDOR）挖掘技巧及实战案例全汇总"
    cur_date = "2019-8-2"
    cur_url = "https://mp.weixin.qq.com/s?__biz=MzI3MTQyNzQxMA%3D%3D&mid=2247484165&idx=1&sn=c5a323c138e2127470872c8756acbf81&scene=45#wechat_redirect"

    dir_name = "./mhtml/{}/".format(gzh_name)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    filename = "[{}]-{}-{}".format(gzh_name, cur_date, cur_tit)
    filename =  dir_name + filename + ".mhtml"
    print(filename)
    if not os.path.exists(filename):
       getMHTML(cur_url, filename)

