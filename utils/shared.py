import psycopg2
from psycopg2 import sql
from config.settings import TABLE_NUM


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
