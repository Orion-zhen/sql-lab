import psycopg2
from psycopg2 import sql
from utils.shared import splitter
from config.settings import TABLE_NUM


def make_queries(
    conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor
):
    """第三大题第一小题, 执行若干查询指令

    Args:
        conn (psycopg2.extensions.connection): 数据库连接
        cursor (psycopg2.extensions.cursor): 数据库执行指针
    """    
    
    t1 = "查询电子工程系(EE)所开课程的课程编号、课程名称及学分数"
    q1 = f"SELECT C#, CNAME, CREDIT FROM C{TABLE_NUM} WHERE C# LIKE 'EE-%';"

    t2 = "查询未选修课程“CS-02”的女生学号及其已选各课程编号、成绩"
    q2 = f"""
    SELECT S.S#, SC.C#, SC.GRADE
    FROM S{TABLE_NUM} AS S
    JOIN SC{TABLE_NUM} AS SC ON S.S# = SC.S#
    LEFT JOIN SC{TABLE_NUM} AS SC_CS02 ON SC_CS02.S# = S.S# AND SC_CS02.C# = 'CS-02'
    WHERE SC_CS02.C# IS NULL AND S.SEX = '女';
    """

    t3 = "查询 2002 年~2003 年出生学生的基本信息"
    q3 = f"""
    SELECT * FROM S{TABLE_NUM}
    WHERE BDATE BETWEEN '2002-01-01' AND '2003-12-31';
    """

    t4 = "查询每位学生的学号、学生姓名及其已选修课程的学分总数"
    q4 = f"""
    SELECT 
        S.S#, 
        S.SNAME, 
        SUM(C.CREDIT) AS TOTAL_CREDIT
    FROM 
        S{TABLE_NUM} AS S
    JOIN 
        SC{TABLE_NUM} AS SC ON S.S# = SC.S#
    JOIN 
        C{TABLE_NUM} AS C ON SC.C# = C.C#
    GROUP BY 
        S.S#, 
        S.SNAME;
    """

    t5 = "查询选修课程“CS-01”的学生中成绩第二高的学生学号"
    q5 = f"""
    SELECT SC.S#
    FROM SC{TABLE_NUM} AS SC
    JOIN C{TABLE_NUM} AS C ON SC.C# = C.C#
    WHERE C.C# = 'CS-01'
    AND SC.GRADE < (SELECT MAX(GRADE) FROM SC{TABLE_NUM} WHERE C# = 'CS-01' LIMIT 1)
    ORDER BY SC.GRADE DESC
    LIMIT 1;
    """

    t6 = "查询平均成绩超过“王涛“同学的学生学号、姓名和平均成绩, 并按学号进行降序排列"
    q6 = f"""
    WITH WangTaoAverage AS (
        SELECT AVG(GRADE) AS avg_grade
        FROM SC{TABLE_NUM}
        JOIN S{TABLE_NUM} ON SC{TABLE_NUM}.S# = S{TABLE_NUM}.S#
        WHERE S{TABLE_NUM}.SNAME = '王涛'
    )
    SELECT 
        S.S#, 
        S.SNAME, 
        AVG(SC.GRADE) AS avg_grade
    FROM 
        S{TABLE_NUM} AS S
    JOIN 
        SC{TABLE_NUM} AS SC ON S.S# = SC.S#
    GROUP BY 
        S.S#, 
        S.SNAME
    HAVING 
        AVG(SC.GRADE) > (SELECT avg_grade FROM WangTaoAverage)
    ORDER BY 
        S.S# DESC;
    """

    t7 = "查询选修了计算机专业全部课程(课程编号为“CS-××”)的学生姓名及已获得的学分总数"
    q7 = f"""
    WITH CS_Courses AS (
        SELECT C# 
        FROM C{TABLE_NUM} 
        WHERE C# LIKE 'CS-%'
    ),
    Students_With_All_CS_Courses AS (
        SELECT SC.S#
        FROM SC{TABLE_NUM} SC
        JOIN CS_Courses CC ON SC.C# = CC.C#
        GROUP BY SC.S#
        HAVING COUNT(DISTINCT SC.C#) = (SELECT COUNT(*) FROM CS_Courses)
    )
    SELECT 
        S.SNAME, 
        SUM(C.CREDIT) AS Total_Credits
    FROM 
        S{TABLE_NUM} S
    JOIN 
        Students_With_All_CS_Courses SwA ON S.S# = SwA.S#
    JOIN 
        SC{TABLE_NUM} SC ON S.S# = SC.S#
    JOIN 
        C{TABLE_NUM} C ON SC.C# = C.C#
    GROUP BY 
        S.SNAME;
    """
    
    t8 = "查询选修了 3 门以上课程(包括 3 门)的学生中平均成绩最高的同学学号及姓名"
    q8 = f"""
    SELECT 
        S.S#, 
        S.SNAME
    FROM 
        S{TABLE_NUM} AS S
    JOIN 
        SC{TABLE_NUM} AS SC ON S.S# = SC.S#
    GROUP BY 
        S.S#, 
        S.SNAME
    HAVING 
        COUNT(SC.C#) >= 3
    ORDER BY 
        AVG(SC.GRADE) DESC
    LIMIT 1;
    """
    
    tasks = [t1, t2, t3, t4, t5, t6, t7, t8]
    queries = [q1, q2, q3, q4, q5, q6, q7, q8]
    
    for task, query in zip(tasks, queries):
        print(task)
        cursor.execute(query)
        for row in cursor.fetchall():
            print(row)
        splitter()
