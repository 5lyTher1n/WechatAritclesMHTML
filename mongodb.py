from pymongo import MongoClient

# from Url2MHtml import get_URLList,replace_name

import datetime
import time

def add_record(gzh_name, data):
    mg_cnn = MongoClient('localhost')
    db = mg_cnn.wechat_articles[gzh_name]
    dtime = datetime.datetime.now()
    utime = time.mktime(dtime.timetuple())
    create_time = datetime.datetime.fromtimestamp(utime)
    print(create_time)
    url = data[0]
    tit = data[1]
    date = data[2]
    tmp = {
        'url': url,
        'title': tit,
        'date': date,
        'create_time': create_time
    }

    flag = db.count_documents({"url":url}, limit=1)
    print(flag)
    if flag == 0:
        db.insert_one(tmp)
        print(tmp)


def get_last_record(gzh_name):

    # xlsx_path = gzh_name + ".xlsx"
    # info_list = get_URLList(xlsx_path)

    mg_cnn = MongoClient('localhost')
    db = mg_cnn.wechat_articles[gzh_name]
    # db.drop()
    dtime = datetime.datetime.now()
    utime = time.mktime(dtime.timetuple())
    create_time = datetime.datetime.fromtimestamp(utime)
    print(create_time)
    # for url, tit, date in info_list:
    #     tit = replace_name(tit)
    #     tmp = {
    #         'url': url,
    #         'title': tit,
    #         'date': date,
    #         'create_time': create_time
    #     }
    #     db.insert_one(tmp)

        # last_date = db.wechat_articles[gzh_name].find().sort({date:1})
    records = db.find().sort('-date')
    last_date = records[0]['date']
    print("db last_date:", last_date)
    last_record_url = []
    last_record_title = []
    # print(records)
    for e in records:
        if (e['date'] == last_date):
            last_record_url.append(e['url'])
            last_record_title.append(e['title'])
            print(e)
            continue
        break

    print(last_record_title)
    print(last_record_url)
    return last_date,last_record_url,last_record_title

if __name__ == "__main__":
    gzh_name = "迪哥讲事"
    # last_date,last_record_url,last_record_title = get_last_record(gzh_name)
    add_record(gzh_name,[1,2,3])
