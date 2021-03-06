import pymysql
import hashlib
import cn_time

db = pymysql.connect(
host='127.0.0.1',
user='root',
password='',
db='xiaodown',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor
)

cursor = db.cursor()

def sql_chaxun(url):
    # 生成hash值
    md5 = hashlib.md5()
    md5.update(str(url).encode('utf-8'))
    url_hash = md5.hexdigest()

    # 查询
    sql = "SELECT * FROM sexinsex WHERE url_hash='"+str(url_hash)+"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    db.commit()

    if len(res):
        cx_res = 'cunzai'
        pass
    else:
        cx_res = 'bucunzai'

    db.close()
    return cx_res


def sql_charu(url):
    # 生成hash值
    md5 = hashlib.md5()
    md5.update(str(url).encode('utf-8'))
    url_hash = md5.hexdigest()

    # 插入到mysql
    sql = "INSERT INTO sexinsex (`ID`, `url`, `url_hash`) VALUES (NULL, '" + \
        str(url) + "', '" + str(url_hash) + "');"
    cursor.execute(sql)
    print(cn_time.thetime()+'自增id为：' + str(db.insert_id()))
    db.commit()
    db.close()
