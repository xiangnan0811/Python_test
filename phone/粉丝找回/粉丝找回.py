import time
import requests
import pandas as pd


def get_func_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} 花费时间: {end - start}')
        return result
    return wrapper


@get_func_time
def get_user(limit, offset):

    cookies = {
        'PHPSESSID': 'miamvcqoacdd5ndpclmjcob86u',
    }

    headers = {
        'Proxy-Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Content-Type': 'application/json',
        'Referer': 'http://cw.ggyouhui.com/index/fans/retrieve',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('sort', 'id'),
        ('order', 'asc'),
        ('offset', f'{offset}'),
        ('limit', f'{limit}'),
        ('filter', '{}'),
        ('op', '{}'),
        ('_', f'{int(time.time()*1000)}'),
    )

    response = requests.get('http://cw.ggyouhui.com/index/fans/retrieve/index', headers=headers, params=params, cookies=cookies, verify=False)

    return pd.DataFrame(response.json()['rows'])


@get_func_time
def df_write_to_csv(df):
    df.to_csv('用户.csv', index=False, encoding='utf_8_sig')


if __name__ == "__main__":
    res = get_user(10400, 0)
    print(res)
    df_write_to_csv(res)
