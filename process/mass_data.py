import json
import random
import psycopg2
from tqdm import tqdm
from psycopg2 import sql
from config.settings import TABLE_NUM


def mass_insert(
    conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor
) -> None:
    with open("s_data.json", "r", encoding="utf-8") as f:
        s_data = json.load(f)
    with open("c_data.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
    with open("sc_data.json", "r", encoding="utf-8") as f:
        sc_data = json.load(f)

    s_rows = []
    for s in tqdm(s_data):
        s_rows.append((s["id"], s["name"], s["sex"], s["bdate"], s["height"], s["dorm"]))

    c_rows = []
    for c in tqdm(c_data):
        c_rows.append((c["id"], c["name"], c["period"], c["credit"], c["teacher"]))

    sc_rows = []
    for sc in tqdm(sc_data):
        sc_rows.append((sc["s_id"], sc["c_id"], sc["grade"]))

    insert_s = f"""
    INSERT INTO S{TABLE_NUM} (S#, SNAME, SEX, BDATE, HEIGHT, DORM)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    insert_c = f"""
    INSERT INTO C{TABLE_NUM} (C#, CNAME, PERIOD, CREDIT, TEACHER)
    VALUES (%s, %s, %s, %s, %s);
    """
    insert_sc = f"""
    INSERT INTO SC{TABLE_NUM} (S#, C#, GRADE)
    VALUES (%s, %s, %s);
    """
    cursor.executemany(sql.SQL(insert_s), s_rows)
    cursor.executemany(sql.SQL(insert_c), c_rows)
    cursor.executemany(sql.SQL(insert_sc), sc_rows)
    conn.commit()


def delete_lower(
    conn: psycopg2.extensions.connection, cursor: psycopg2.extensions.cursor, number=200
):
    cursor.execute(f"SELECT S#, C# FROM SC{TABLE_NUM} WHERE GRADE < 60")
    low_grade_records = cursor.fetchall()

    random_records = random.sample(
        low_grade_records, min(number, len(low_grade_records))
    )
    for record in tqdm(random_records):
        cursor.execute(
            f"DELETE FROM SC{TABLE_NUM} WHERE S# = %s AND C# = %s",
            (record[0], record[1]),
        )

        conn.commit()
