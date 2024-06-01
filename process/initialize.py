import psycopg2
from psycopg2 import sql
from config.settings import TABLE_NUM


def init_tables(
    conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor
):
    """创建初始的3个表(学生表, 课程表, 学生选课表)

    Args:
        conn (psycopg2.extensions.connection): 数据库连接
        cursor (psycopg2.extensions.cursor): 数据库执行指针
    """    
    
    # 创建学生表
    create_table_s = f"""
    CREATE TABLE S{TABLE_NUM} (
        S# VARCHAR(20) PRIMARY KEY,
        SNAME VARCHAR(50),
        SEX VARCHAR(10),
        BDATE DATE,
        HEIGHT FLOAT,
        DORM VARCHAR(50)
    );
    """

    # 创建课程表
    create_table_c = f"""
    CREATE TABLE C{TABLE_NUM} (
        C# VARCHAR(20) PRIMARY KEY,
        CNAME VARCHAR(100),
        PERIOD INT,
        CREDIT FLOAT,
        TEACHER VARCHAR(50)
    );
    """

    # 创建学生选课表
    create_table_sc = f"""
    CREATE TABLE SC{TABLE_NUM} (
        S# VARCHAR(20),
        C# VARCHAR(20),
        GRADE FLOAT,
        PRIMARY KEY (S#, C#),
        FOREIGN KEY (S#) REFERENCES S{TABLE_NUM}(S#),
        FOREIGN KEY (C#) REFERENCES C{TABLE_NUM}(C#)
    );
    """

    cursor.execute(sql.SQL(create_table_s))
    cursor.execute(sql.SQL(create_table_c))
    cursor.execute(sql.SQL(create_table_sc))
    conn.commit()


def insert_init_data(
    conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor
):
    """向初始表中插入初始数据

    Args:
        conn (psycopg2.extensions.connection): 数据库连接
        cursor (psycopg2.extensions.cursor): 数据库执行指针
    """    
    
    insert_s = f"""
    INSERT INTO S{TABLE_NUM} (S#, SNAME, SEX, BDATE, HEIGHT, DORM)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    student_data = [
        ("01032010", "王涛", "男", "2003-4-5", 1.72, "东6舍221"),
        ("01032023", "孙文", "男", "2004-6-10", 1.80, "东6舍221"),
        ("01032001", "张晓梅", "女", "2004-11-17", 1.58, "东1舍312"),
        ("01032005", "刘静", "女", "2003-1-10", 1.63, "东1舍312"),
        ("01032112", "董蔚", "男", "2003-2-20", 1.71, "东6舍221"),
        ("03031011", "王倩", "女", "2004-12-20", 1.66, "东2舍104"),
        ("03031014", "赵思扬", "男", "2002-6-6", 1.85, "东18舍421"),
        ("03031051", "周剑", "男", "2002-5-8", 1.68, "东18舍422"),
        ("03031009", "田菲", "女", "2003-8-11", 1.60, "东2舍104"),
        ("03031033", "蔡明明", "男", "2003-3-12", 1.75, "东18舍423"),
        ("03031056", "曹子衿", "女", "2004-12-15", 1.65, "东2舍305"),
    ]

    insert_c = f"""
    INSERT INTO C{TABLE_NUM} (C#, CNAME, PERIOD, CREDIT, TEACHER)
    VALUES (%s, %s, %s, %s, %s);
    """
    class_data = [
        ("CS-01", "数据结构", 60, 3, "张军"),
        ("CS-02", "计算机组成原理", 80, 4, "王亚伟"),
        ("CS-04", "人工智能", 40, 2, "李蕾"),
        ("CS-05", "深度学习", 40, 2, "崔昀"),
        ("EE-01", "信号与系统", 60, 3, "张明"),
        ("EE-02", "数字逻辑电路", 100, 5, "胡海东"),
        ("EE-03", "光电子学与光子学", 40, 2, "石韬"),
    ]

    insert_sc = f"""
    INSERT INTO SC{TABLE_NUM} (S#, C#, GRADE)
    VALUES (%s, %s, %s);
    """
    sc_data = [
        ("01032010", "CS-01", 82.0),
        ("01032010", "CS-02", 91.0),
        ("01032010", "CS-04", 83.5),
        ("01032001", "CS-01", 77.5),
        ("01032001", "CS-02", 85.0),
        ("01032001", "CS-04", 83.0),
        ("01032005", "CS-01", 62.0),
        ("01032005", "CS-02", 77.0),
        ("01032005", "CS-04", 82.0),
        ("01032023", "CS-01", 55.0),
        ("01032023", "CS-02", 81.0),
        ("01032023", "CS-04", 76.0),
        ("01032112", "CS-01", 88.0),
        ("01032112", "CS-02", 91.5),
        ("01032112", "CS-04", 86.0),
        ("01032112", "CS-05", None),
        ("03031033", "EE-01", 93.0),
        ("03031033", "EE-02", 89.0),
        ("03031009", "EE-01", 88.0),
        ("03031009", "EE-02", 78.5),
        ("03031011", "EE-01", 91.0),
        ("03031011", "EE-02", 86.0),
        ("03031051", "EE-01", 78.0),
        ("03031051", "EE-02", 58.0),
        ("03031014", "EE-01", 79.0),
        ("03031014", "EE-02", 71.0),
    ]

    cursor.executemany(sql.SQL(insert_s), student_data)
    cursor.executemany(sql.SQL(insert_c), class_data)
    cursor.executemany(sql.SQL(insert_sc), sc_data)
    conn.commit()
