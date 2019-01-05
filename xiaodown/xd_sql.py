import pymysql
import hashlib
import xd_time
import dribbble

def sql_chaxun(db_name,biao_name,url):
    db = pymysql.connect(
        host='127.0.0.1',
        user='xiaodown',
        password='199011',
        db=db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = db.cursor()

    # 生成hash值
    md5 = hashlib.md5()
    md5.update(str(url).encode('utf-8'))
    url_hash = md5.hexdigest()

    # 查询
    sql = "SELECT * FROM "+biao_name+" WHERE url_hash='"+str(url_hash)+"'"
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

def sql_charu(db_name,biao_name,url):
    db = pymysql.connect(
        host='127.0.0.1',
        user='xiaodown',
        password='199011',
        db=db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = db.cursor()

    # 生成hash值
    md5 = hashlib.md5()
    md5.update(str(url).encode('utf-8'))
    url_hash = md5.hexdigest()

    # 插入到mysql
    sql = "INSERT INTO " + biao_name + " (`ID`, `url`, `url_hash`) VALUES (NULL, '" + str(url) + "', '" + str(
        url_hash) + "');"
    cursor.execute(sql)
    dribbble.shuchu('自增id为',str(db.insert_id()))
    db.commit()
    db.close()