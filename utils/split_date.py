from datetime import datetime, timedelta


def split_date(start, end, time_interval):
    """
    :param start: 开始时间
    :param end: 结束时间
    :param time_interval: 时间间隔
    :return:
    """
    time_format = "%Y-%m-%d"
    start_time = datetime.strptime(start[:10], time_format)
    end_time = datetime.strptime(end[:10], time_format)
    time_list = []
    while (end_time - start_time) >= timedelta(minutes=time_interval):
        new_start = start_time + timedelta(minutes=time_interval)
        time_list.append((start_time.strftime(time_format), (new_start - timedelta(seconds=1)).strftime(time_format)))
        start_time = new_start
    if end_time >= start_time:
        time_list.append((start_time.strftime(time_format), end_time.strftime(time_format)))
    return time_list


if __name__ == '__main__':
    start_time = "2024-01-01 00:00:00"
    end_time = "2024-01-03 00:00:00"
    time_interval = 60 * 24 * 2
    print(split_date(start_time, end_time, time_interval))
