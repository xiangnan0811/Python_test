import datetime


def parse_time_string(txt):
    def next_part(p, max_char):
        e = len(txt)
        r = 0
        begin = False

        while p < e:
            c = ord(txt[p])
            p += 1

            if 0x30 <= c <= 0x39:
                if not begin:
                    begin = True
                    e = min(len(txt), p + max_char - 1)
                r = r * 10 + c - 0x30
            else:
                if begin:
                    return r, p

        return r, p

    if txt is None or len(txt) < 4:
        raise RuntimeError(f'日期格式错误: {txt}')

    p = 0
    year, p = next_part(p, 4)
    month, p = next_part(p, 2)
    day, p = next_part(p, 2 if year > 100 else 4)
    hour, p = next_part(p, 2)
    minute, p = next_part(p, 2)
    second, p = next_part(p, 2)
    mis, p = next_part(p, 6)

    if (year < 100 <= day) or (month > 12 and year < 100):
        year, month, day = day, year, month

    day = day or 1
    year = year if year >= 100 else year + 2000
    if month > 12 and day < 10:
        day = int((month % 10) * 10 + day)
        month = int(month / 10)

    return datetime.datetime(year, month, day, hour, minute, second, mis)

