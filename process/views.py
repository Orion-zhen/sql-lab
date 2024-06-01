import psycopg2
from psycopg2 import sql
from config.settings import TABLE_NUM


def create_views(conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor):
    """第三大题第五小题 创建视图

    Args:
        conn (psycopg2.extensions.connection): 数据库连接
        cursor (psycopg2.extensions.cursor): 数据库执行指针
    """
    
    # 1. 居住在“东 18 舍”的男生视图, 包括学号、姓名、出生日期、身高等属性
    q1 = f"""
    CREATE VIEW Boys_In_East18 AS
    SELECT 
        S#, 
        SNAME, 
        BDATE, 
        HEIGHT,
        DORM
    FROM 
        S{TABLE_NUM}
    WHERE 
        DORM LIKE '东18舍%' AND SEX = '男';
    """
    
    # 2. “张明”老师所开设课程情况的视图,包括课程编号、课程名称、平均成绩等属性
    q2 = f"""
    CREATE VIEW Courses_Taught_By_ZhangMing AS
    SELECT 
        C.C#,
        C.CNAME,
        AVG(SC.GRADE) AS AverageGrade
    FROM 
        C{TABLE_NUM} AS C
    JOIN 
        SC{TABLE_NUM} AS SC ON C.C# = SC.C#
    WHERE 
        C.TEACHER = '张明'
    GROUP BY 
        C.C#, 
        C.CNAME;
    """
    
    # 3. 所有选修了“人工智能”课程的学生视图,包括学号、姓名、成绩等属性
    q3 = f"""
    CREATE VIEW Students_Who_Took_AI AS
    SELECT 
        S.S#,
        S.SNAME,
        SC.GRADE
    FROM 
        S{TABLE_NUM} AS S
    JOIN 
        SC{TABLE_NUM} AS SC ON S.S# = SC.S#
    WHERE 
        SC.C# = 'CS-04';
    """
    
    queries = [q1, q2, q3]
    for query in queries:
        cursor.execute(query)
    conn.commit()