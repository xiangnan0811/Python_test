import time
from datetime import datetime

import requests
from lxml import etree

headers = {
    "Cookie": "",
    'Referer': 'https://list1.mysteel.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}


def request(url):
    time.sleep(0.05)
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    return response


def get_article_list_page():
    url = 'https://xian.mysteel.com/'
    response = request(url)
    # 通过xpath获取 class="news-box f-l mr-30 H-350" 的section标签下的a标签
    html = etree.HTML(response.text)
    a = html.xpath('//section[@class="news-box f-l mr-30 H-350"]/h3/a')
    for i in a:
        text = i.xpath('./text()')[0].strip()
        href = i.xpath('./@href')[0].strip()
        if '西安建筑钢材价格' in text:
            return href
    return None


def get_article_detail_pages(url, start_date):
    if not start_date:
        now = datetime.now()
        start = datetime(now.year, now.month, now.day)
    else:
        start = datetime.strptime(f"{start_date}", '%Y-%m-%d')
    pages = []
    next_article_page = None
    break_flag = False
    response = request(url)
    html = etree.HTML(response.text)
    # 通过 xpath 获取 class 为 nlist 的 ul 标签下的有class属性的 li 标签
    lis = html.xpath('//ul[@class="nlist"]/li[@data-val]')
    # for 循环获取 li 下 a 标签的 text,跳过 text 中没有 '西安市场建筑钢材价格行情' 的 li 标签
    for li in lis:
        text = li.xpath('./a/text()')[0].strip()
        href = li.xpath('./a/@href')[0].strip()
        if '西安市场建筑钢材价格行情' in text:
            date_str = href.split('/')[-2]
            if len(date_str) < 6:
                continue
            article_date = datetime.strptime(f"{date_str}", '%y%m%d%H')
            if article_date < start:
                break_flag = True
                break
            else:
                # print(f"详情页title: {text}, url: {href}")
                pages.append(href)

    # 获取下一页的链接
    if not break_flag:
        # 获取 class 为 current 的 span标签的所有兄弟 a 标签
        next_page = html.xpath('//span[@class="current"]/following-sibling::a')
        # for 循环获取 a 标签的 text,跳过 text 中没有 '下一页' 的 a 标签
        for a in next_page:
            text = a.xpath('./text()')[0].strip()
            if '下一页' in text:
                href = a.xpath('./@href')[0].strip()
                next_url = f"https://list1.mysteel.com{href}"
                print(f"列表页下一页 url: {next_url}")
                next_article_page = next_url
                break
    return pages, next_article_page


def parse_detail_page(url):
    response = request(url)
    html = etree.HTML(response.text)
    trs = html.xpath('//table[@id="marketTable"]/tr[@table-row-id]')
    date_str = url.split('/')[-2]
    date_str = datetime.strptime(f"{date_str}", '%y%m%d%H').strftime('%Y-%m-%d %H')
    # for 循环获取 tr 下 td 标签里 data-type 为 place的文本
    res = []
    for tr in trs:
        # 品名
        breed= tr.xpath('./td[@data-type="breed"]/text()')[0].strip()
        # 规格
        spec = tr.xpath('./td[@data-type="spec"]/text()')[0].strip()
        # 材质
        material = tr.xpath('./td[@data-type="material"]/text()')[0].strip()
        # 产地
        place = tr.xpath('./td[@data-type="place"]/text()')[0].strip()
        # 价格
        price = tr.xpath('./td[@data-type="price"]/text()')[0].strip()
        # 涨跌
        raise_s = tr.xpath('./td[@data-type="raise"]/text()')[0].strip()
        if material == 'HPB300' and spec == 'Φ8' and place == '龙钢':
            data = (date_str, breed, spec, material, place, price, raise_s)
            print(data)
            res.append(data)
        if material == 'HRB400E' and spec in ('Φ12', 'Φ20') and place == '龙钢':
            data = (date_str, breed, spec, material, place, price, raise_s)
            print(data)
            res.append(data)
    return res


def main():
    print(f" ------------ 程序开始运行,当前时间: {datetime.now()} ------------ ")
    x = input('程序运行会将结果保存在当前目录下的data.csv文件中,请确保当前目录下没有data.csv文件,否则会覆盖程序当前目录下的data.csv,确认完毕按回车继续\n')
    date_str = input('请输入抓取数据起始日期(格式: 2021-07-01),输入完毕按回车结束,直接回车只抓今天的\n')
    cookie_str = input('请输入cookie,输入完毕按回车结束\n')
    if cookie_str:
        headers.update({'Cookie': cookie_str})
    result = []
    result.append(('时间', '品名', '规格', '材质', '产地', '价格', '涨跌'))
    article_list_page = get_article_list_page()
    if not article_list_page:
        print('未找到西安建筑钢材价格的文章列表页')
        return
    article_detail_pages, next_article_page = [], article_list_page
    while next_article_page:
        pages, next_article_page = get_article_detail_pages(next_article_page, date_str)
        article_detail_pages.extend(pages)
    for page in article_detail_pages:
        res = parse_detail_page(page)
        result.extend(res)
    if len(result) > 1:
        with open('./data.csv', 'w', encoding='utf-8-sig') as f:
            for i in result:
                f.write(','.join(i) + '\n')
    print(f'抓取完成,共抓取{len(result) - 1}条数据,结果保存在当前目录下的data.csv文件中')
    print(f" ------------ 程序结束运行,当前时间: {datetime.now()} ------------ ")


if __name__ == '__main__':
    main()
