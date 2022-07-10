from pymongo import MongoClient

from Url2MHtml import get_URLList,replace_name

def get_last_record(gch_name):

    xlsx_path = gzh_name + ".xlsx"
    info_list = get_URLList(xlsx_path)

    mg_cnn = MongoClient('localhost')
    db = mg_cnn.wechat_articles[gzh_name]
    for url, tit, date in info_list:
        tit = replace_name(tit)
        tmp = {
            'url': url,
            'title': tit,
            'date': date
        }
        # db.insert_one(tmp)

        # last_date = db.wechat_articles[gzh_name].find().sort({date:1})
    records = db.find().sort('-date')
    last_date = records[0]['date']
    print(last_date)
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
    return last_record_url,last_record_title

if __name__ == "__main__":
    gzh_name = "迪哥讲事"
