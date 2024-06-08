import json
import random
import psycopg2
from tqdm import tqdm
from faker import Faker
from psycopg2 import sql
from config.settings import TABLE_NUM, S_MAX, C_MAX, SC_MAX

C_NAME_CANDIDATES = [
    "数据科学与机器学习",
    "网络安全基础",
    "Java编程语言",
    "Python数据分析",
    "云计算架构",
    "人工智能",
    "计算机视觉",
    "数据库管理系统",
    "网络管理基础",
    "软件开发方法",
    "数据挖掘",
    "机器学习算法",
    "计算机网络安全",
    "信息安全管理",
    "IT项目管理",
    "计算机科学基础",
    "数据结构",
    "算法设计",
    "计算机图形学",
    "Web开发技术",
    "数据库设计",
    "计算机网络协议",
    "软件测试技术",
]


def splitter(width=50):
    print("\n" + "=" * width + "\n")


def show_all(conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor):
    """展示所有表

    Args:
        conn (psycopg2.extensions.connection): 数据库连接
        cursor (psycopg2.extensions.cursor): 数据库执行指针
    """

    # 查询所有表
    cursor.execute(
        sql.SQL(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
        )
    )
    tables = [row[0] for row in cursor.fetchall()]
    print("\n==============================All Tables==============================\n")
    print(tables)

    for table in tables:
        get_table = f"SELECT * FROM {table}"
        cursor.execute(sql.SQL(get_table))
        rows = cursor.fetchall()
        print(f"\n=============================={table}============================\n")
        for row in rows:
            print(row)


def delete_all(
    conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor
):
    """删除数据库中所有的表和视图

    Args:
        conn (psycopg2.extensions.connection): 数据库连接
        cursor (psycopg2.extensions.cursor): 数据库执行指针
    """

    # 查询所有表
    cursor.execute(
        sql.SQL(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
        )
    )
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        try:
            delete_table = f"DROP TABLE IF EXISTS {table} CASCADE;"
            cursor.execute(sql.SQL(delete_table))
        except:
            delete_view = f"DROP VIEW IF EXISTS {table} CASCADE;"
            cursor.execute(sql.SQL(delete_view))
    conn.commit()


def gen_mass_data(
    s_lines=S_MAX,
    c_lines=C_MAX,
    sc_lines=SC_MAX,
) -> None:

    students = []
    print("Generating students...")
    for _ in tqdm(range(s_lines)):
        s_name = Faker("zh_CN").name()
        s_id = ""
        for _ in range(8):
            s_id += str(random.randint(0, 9))
        s_sex = random.choice(["男", "女"])
        s_bdate = str(Faker("zh_CN").date_of_birth(minimum_age=18, maximum_age=22))
        s_height = float(random.randint(150, 200)) / 100.0
        s_dorm = (
            random.choice(["东", "西"])
            + str(random.randint(1, 20))
            + "舍"
            + str(random.randint(100, 400))
        )

        students.append(
            {
                "name": s_name,
                "id": s_id,
                "sex": s_sex,
                "bdate": s_bdate,
                "height": s_height,
                "dorm": s_dorm,
            }
        )

    cources = []
    seen_c_ids = set()
    print("Generating cources...")
    for _ in tqdm(range(c_lines)):
        while True:
            prefix = random.choice(["CS-", "EE-"])
            c_id = prefix + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
            if c_id not in seen_c_ids:
                seen_c_ids.add(c_id)
                break
        c_name = random.choice(C_NAME_CANDIDATES)
        c_period = random.choice(["60", "80", "100", "40", "64", "32"])
        c_credit = random.randint(1, 5)
        c_teacher = Faker("zh_CN").name()

        cources.append(
            {
                "id": c_id,
                "name": c_name,
                "period": c_period,
                "credit": c_credit,
                "teacher": c_teacher,
            }
        )

    sc_list = []
    seen_sc = set()
    print("Generating sc_list...")
    for _ in tqdm(range(sc_lines)):
        while True:
            s_id = random.choice(students)["id"]
            c_id = random.choice(cources)["id"]
            if (s_id, c_id) not in seen_sc:
                seen_sc.add((s_id, c_id))
                break
        grade = random.randint(0, 100)

        sc_list.append(
            {
                "s_id": s_id,
                "c_id": c_id,
                "grade": grade,
            }
        )

    with open("s_data.json", "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=4)
    with open("c_data.json", "w", encoding="utf-8") as f:
        json.dump(cources, f, ensure_ascii=False, indent=4)
    with open("sc_data.json", "w", encoding="utf-8") as f:
        json.dump(sc_list, f, ensure_ascii=False, indent=4)
