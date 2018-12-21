import pymysql
import hashlib

def sql(db_name,biao_name,url):
    db = pymysql.connect(
        host='localhost',
        user='root',
        password='',
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

        # 插入到mysql
        sql = "INSERT INTO "+biao_name+" (`ID`, `url`, `url_hash`) VALUES (NULL, '"+str(url)+"', '"+str(url_hash)+"');"
        cursor.execute(sql)
        db.commit()

    db.close()
    return cx_res