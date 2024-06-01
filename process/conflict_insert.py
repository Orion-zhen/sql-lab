import psycopg2
from psycopg2 import sql
from config.settings import TABLE_NUM


def conflict_insert(
    conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor
):
    """第三大题第二小题 分别在 S×××和 C×××表中加入记录(‘01032005’, ‘刘竞’, ‘男’, ‘2003-12-10’, 1.75, ‘东 14 舍 312’)及(‘CS-03’, “离散数学”, 64, 4, ‘陈建明’)

    Args:
        conn (psycopg2.extensions.connection): 数据库连接
        cursor (psycopg2.extensions.cursor): 数据库命令执行指针
    """
    
    insert_s = f"""
    INSERT INTO S{TABLE_NUM} (S#, SNAME, SEX, BDATE, HEIGHT, DORM) 
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    insert_c = f"""
    INSERT INTO C{TABLE_NUM} (C#, CNAME, PERIOD, CREDIT, TEACHER) 
    VALUES (%s, %s, %s, %s, %s);
    """

    student_data = ("01032005", "刘竞", "男", "2003-12-10", 1.75, "东14舍312")
    course_data = ("CS-03", "离散数学", 64, 4, "陈建明")

    try:
        cursor.execute(sql.SQL(insert_s), student_data)
        cursor.execute(sql.SQL(insert_c), course_data)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
