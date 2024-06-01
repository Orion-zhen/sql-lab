from utils.connection import conn, cursor
from utils.shared import delete_all, show_all
from process.initialize import init_tables, insert_init_data
from process.queries import make_queries
from process.conflict_insert import conflict_insert
from process.delete_one import delete_one
from process.update_one import update_one
from process.views import create_views


if __name__ == "__main__":
    print("正在初始化数据库...\n")
    delete_all(conn, cursor)

    print("[第一大题] 正在初始化表...\n")
    init_tables(conn, cursor)

    print("[第二大题] 正在插入初始数据...\n")
    insert_init_data(conn, cursor)
    show_all(conn, cursor)

    print("[第三大题第一小题] 正在执行查询...\n")
    make_queries(conn, cursor)

    print("[第三大题第二小题] 正在执行冲突插入...\n")
    conflict_insert(conn, cursor)

    print("[第三大题第三小题] 正在删除一个表项...\n")
    delete_one(conn, cursor)

    print("[第三大题第四小题] 正在更新一个表项...\n")
    update_one(conn, cursor)

    print("[第三大题第五小题] 正在创建视图...\n")
    create_views(conn, cursor)

    print("展示所有表项...\n")
    show_all(conn, cursor)

    cursor.close()
    conn.close()
