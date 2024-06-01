import psycopg2
from psycopg2 import sql
from config.settings import TABLE_NUM


def delete_one(conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor):
    """第三大题第三小题 将 S×××表中已修学分数大于 60 的学生记录删除

    Args:
        conn (psycopg2.extensions.connection): 数据库连接
        cursor (psycopg2.extensions.cursor): 数据库执行指针
    """
    
    delete_s = f"""
    DELETE FROM S{TABLE_NUM}
    WHERE S# IN (
        SELECT S#
        FROM C004
        GROUP BY S#
        HAVING SUM(CREDIT) > 60
    );
    """
    cursor.execute(sql.SQL(delete_s))
    conn.commit()