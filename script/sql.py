import pymysql
import hashlib

def sql(dbname,url):
    db = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='xiaodown',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = db.cursor()

    # 生成hash值
    md5 = hashlib.md5()
    md5.update(str(url).encode('utf-8'))
    url_hash = md5.hexdigest()

    # 查询
    sql = "SELECT * FROM "+dbname+" WHERE url_hash='"+str(url_hash)+"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    db.commit()

    if len(res):
        cx_res = 'cunzai'
        pass
    else:
        cx_res = 'bucunzai'

        # 插入到mysql
        sql = "INSERT INTO "+dbname+" (`ID`, `url`, `url_hash`) VALUES (NULL, '"+str(url)+"', '"+str(url_hash)+"');"
        cursor.execute(sql)
        db.commit()

    db.close()
    return cx_res

sql('dribbble','https://www.cnblogs11.com/pycode/p/hashlib0001.12212html')