import pymysql  # 导入 pymysql


def get_db_con():
    db = pymysql.connect (host="**********", user="****",
                          password="*****", db="*******", port=3306, charset='utf8')
    return db


def get_query_db(sql):
    con = get_db_con ()
    cursor = con.cursor ()
    cursor.execute (sql)
    data = cursor.fetchall ()
    cursor.close ()
    con.close ()
    return data


if __name__ == "__main__":
    pass
