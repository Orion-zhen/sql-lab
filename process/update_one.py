import psycopg2
from psycopg2 import sql
from utils.shared import splitter
from config.settings import TABLE_NUM


def update_one(
    conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor
):
    """第三大题第四小题 将“张明”老师负责的“信号与系统”课程的学时数调整为 64, 同时增加一个学分

    Args:
        conn (psycopg2.extensions.connection): 数据库连接
        cursor (psycopg2.extensions.cursor): 数据库执行指针
    """    
    
    update_c = f"""
    UPDATE C{TABLE_NUM}
    SET PERIOD = 64, CREDIT = CREDIT + 1
    WHERE CNAME = '信号与系统' AND TEACHER = '张明';
    """
    cursor.execute(sql.SQL(update_c))
    cursor.execute(
        sql.SQL(f"SELECT * FROM C{TABLE_NUM} WHERE CNAME = '信号与系统' AND TEACHER = '张明';")
    )
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    splitter()