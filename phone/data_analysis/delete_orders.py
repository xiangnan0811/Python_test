#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: xiangnan
@contact: xiangnan0718@gmail.com
@time: 2022/2/23 11:24
@file: delete_orders.py
@desc: 删除订单
"""
import time

import pymysql


def get_connection(host, port, user, password, db):
    """
    获取数据库连接
    :param host:
    :param port:
    :param user:
    :param password:
    :param db:
    :return:
    """
    return pymysql.connect(
        host=host, port=port, user=user, password=password, db=db, charset='utf8'
    )


def get_cursor(connection):
    """
    获取游标
    :param connection:
    :return:
    """
    return connection.cursor()


def search_orders(cursor):
    """
    查找需要删除的订单id
    :param cursor:
    :return:
    """
    # sql = "SELECT id FROM t_order_info_tb WHERE order_type = '饿了么' LIMIT 500"
    sql = "SELECT id FROM t_order_info_tb WHERE uzai_status = 2 LIMIT 500"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def delete_order(cursor, order_id):
    """
    删除订单

    :param:
    :Returns:
    """
    sql = f"DELETE FROM t_order_info_tb WHERE id = {order_id}"
    cursor.execute(sql)
    return cursor.rowcount


def delete_orders(cursor, orders):
    """
    删除订单

    :param:
    :Returns:
    """
    sql = f"DELETE FROM t_order_info_tb WHERE id IN ({orders})"
    cursor.execute(sql)
    return cursor.rowcount


def main():
    """
    主函数
    :return:
    """
    start_at = time.monotonic()
    conn = get_connection("localhost", 3306, "root", "123456", "lxs_item")
    cursor = get_cursor(conn)
    batch = 0
    while order_ids := search_orders(cursor):
        batch += 1
        print(f"{'-' * 50} 第{batch}批次 {'-' * 50}")
        for order_id in order_ids:
            delete_order(cursor, order_id[0])
            print('-' * 100)
            print(f"删除订单成功：{order_id}")
        # order_ids_str = ",".join([str(order_id[0]) for order_id in order_ids])
        # delete_count = delete_orders(cursor, order_ids_str)
        conn.commit()
    cursor.close()
    conn.close()
    print(f"总耗时：{(time.monotonic() - start_at):.2f}s")


if __name__ == '__main__':
    main()
