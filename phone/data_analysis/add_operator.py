#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: xiangnan
@contact: xiangnan0718@gmail.com
@time: 2022/2/23 11:24
@file: add_operator
@desc: 添加运营商、省、市
"""
import time

import pymysql
import requests


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
    return pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')


def get_cursor(connection):
    """
    获取游标
    :param connection:
    :return:
    """
    return connection.cursor()


def search_phone(cursor):
    """
    没有运营商的手机号
    :param cursor:
    :return:
    """
    sql = "SELECT DISTINCT alipay_account FROM phone_alipay WHERE operator IS NULL LIMIT 300"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# def multi_update_phone(cursor, phone_list):
#     """
#     批量更新手机号
#     :param cursor:
#     :param phone_list:
#     :return:
#     """
#     sql = f"""
#         INSERT INTO
#             phone_alipay (alipay_account, operator, province, city, area_code)
#         VALUES
#             {[phone.values() for phone in phone_list]}
#         ON DUPLICATE KEY UPDATE
#             alipay_account=VALUES(alipay_account),
#     """


def update_phone(cursor, operator_result):
    """
    更新手机号
    :param cursor:
    :param operator_result:
    :return:
    """
    sql = f"""
        UPDATE 
            phone_alipay 
        SET 
            operator = '{operator_result["isp"]}', 
            province = '{operator_result["province"]}', 
            city = '{operator_result["city"]}', 
            area_code = {operator_result["area_code"]} 
        WHERE 
            alipay_account = {operator_result["phone"]}
    """
    cursor.execute(sql)
    return cursor.rowcount


def request_operator(phone):
    """
    请求运营商
    :param phone:
    :return:
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    proxies = {
        "http": "http://127.0.0.1:8888",
        "https": "http://127.0.0.1:8888",
    }
    data = {"phone": phone}
    url = "https://api.uutool.cn/phone/location_batch"
    # response = requests.post(url, headers=headers, data=data, proxies=proxies, verify=False)
    response = requests.post(url, headers=headers, data=data, verify=False)
    result = response.json().get("data", {}).get("rows", [])
    return result


def main():
    """
    主函数
    :return:
    """
    start_at = time.monotonic()
    conn = get_connection("localhost", 3306, "root", "123456", "tk")
    cursor = get_cursor(conn)
    batch = 0
    while phones := search_phone(cursor):
        batch += 1
        print(f"{'-' * 50} 第{batch}批次 {'-' * 50}")
        phone_str = ",".join([str(phone[0]) for phone in phones])
        result = request_operator(phone_str)
        for p_res in result:
            try:
                user_count = update_phone(cursor, p_res)
                conn.commit()
                print('-' * 100)
                print(f"更新手机号成功：{p_res['phone']}，对应用户数：{user_count}")
            except Exception as e:
                print(f"更新手机号失败：{p_res['phone']}，错误信息：{e}")
                conn.rollback()
    cursor.close()
    conn.close()
    print(f"总耗时：{(time.monotonic() - start_at):.2f}s")


if __name__ == '__main__':
    main()
