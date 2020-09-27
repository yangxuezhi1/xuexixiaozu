from lxml import etree
from requests import get
import csv
from bs4 import BeautifulSoup
from re import compile,findall


headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 78.0.3904.108Safari / 537.36',
        'Connection': 'close'
    }
def 爬取数据(i):
    """"""
    url = f'https://sh.lianjia.com/zufang/pg{i}/'
    resp = get(url, headers = headers)
    resp.encoding = 'utf-8'
    return resp.text

def 获取数据1(date,sign=0):
    """
    使用bs4进行数据筛选
    :param date: str 字符串类型
    :param sign: 输出类型标志
    :return: list/dict 列表或字典类型
    """
    __dicts__ = {}
    __lst__ = []
    z1 = 0
    bs_r = BeautifulSoup(date, 'html.parser')
    xs = bs_r.find_all('div', class_="content__list--item")
    for i in xs:
        坐标 = []
        楼层 = []
        数量 = []
        房间信息 = ','.join(i.find('div').find('p', class_='content__list--item--title').find('a').text.split())
        房间详情 = i.find('div').find('p', class_='content__list--item--des').text.split()
        房间链接 = f'https://sh.lianjia.com/{i.find("a")["href"]}'
        房间状态 = ','.join(i.find('div').find('p', class_='content__list--item--bottom oneline').text.split())
        价格 = ''.join(i.find('div').find('span',class_='content__list--item-price').text.split())
        for z in 房间详情:
            if '㎡' in z:
                房间面积 = z
            if '-' in z:
                房间地址 = z
            if '室' in z and '厅' in z and '卫' in z:
                房间间数 = z
            if '层' in z:
                楼层.append(z)
            if '间' in z:
                数量.append(z)
            for i in ['东','西','南','北'] :
                if '/'not in z and i in z and '-' not in z:
                    坐标.append(z)
                if i in z and '/'in z:
                    坐标.append(z.split('/')[1])
        if 楼层:
            房间层数 = ','.join(楼层)
        else:
            房间层数 = ''
        if len(数量) > 1:
            可租数量 = 数量[1].split('/')[1]
        elif len(数量) == 1:
            可租数量 = 数量[0].split('/')[1]
        else:
            可租数量 = '1间在租'
        if len(坐标) >= 1 and 坐标:
            房间朝向 = ','.join(坐标)
        else: 房间朝向 = '空'
        __dicts__[z1] = {'房间信息': 房间信息, '房间面积': 房间面积, "房间地址": 房间地址, '房间间数': 房间间数,'房间朝向': 房间朝向,
                         '房间层数': 房间层数, '可租数量': 可租数量, '租房链接': 房间链接, '房间状态': 房间状态, '价格': 价格}
        __lst__.append([房间信息, 房间面积, 房间地址, 房间间数, 房间朝向, 房间层数, 可租数量, 房间链接, 房间状态, 价格])
        z1 += 1
    if sign:
        return __dicts__
    else:
        return __lst__
def 获取数据2(date, sign=0):
    """
    使用Xpath进行数据筛选
    :param date: str 字符串类型
    :param sign: 输出类型标志
    :return: list/dict 列表或字典类型
    """
    __dicts__ = {}
    __lst__ = []

    html = etree.HTML(date)
    #print(len())
    租房URL = html.xpath('//a[@class="content__list--item--aside"]/@href')
    房间信息 = html.xpath('//a[@class="content__list--item--aside"]/@title')
    特点_r = html.xpath('//p[@class="content__list--item--bottom oneline"]')
    详情_r = html.xpath('//p[@class="content__list--item--des"]/text()')
    地址_r = html.xpath('//a[@class="content__list--item--aside"]/@title')
    金额 = html.xpath('//span[@class="content__list--item-price"]/em/text()')
    单位 = html.xpath('//span[@class="content__list--item-price"]/text()')
    地址_l = []
    房间面积 = []
    房间间数 = []
    数量 = []
    坐标 = []
    临时 = []
    for o in 地址_r:
        o = o.replace('·', ' ')
        临时 = o.split(' ')
        if '店' in 临时[2]:
            地址_l.append(','.join([临时[1],临时[2]]))
        地址_l.append(临时[1])
    for o in 详情_r:
        z1 = o.replace('\n', '').replace(' ', '')
        if z1 != '':
            临时.append(z1)
    for o in 特点_r:
        x1 = o.xpath('//i/text()')
        z = ','.join(x1).split('/,')
        特点 = [y for y in z if y !='' ]
    详情_str = ','.join(临时)
    模板 = compile('(\d+㎡.*?卫)')
    详情_l = 模板.findall(详情_str)
    for str in range(len(详情_l )):
        房间详情 = 详情_l[str].split(',')
        for z in 房间详情:
            if '㎡' in z:
                房间面积.append(z)
            if '室' in z:
                房间间数.append(z)
            if '间' in z:
                数量.append(z)
            else:
                数量.append('1间在租')
            for i in ['东', '西', '南', '北']:
                if i in z:
                    坐标.append(z)
                else:
                    坐标.append('空')
        __dicts__[str] = {'房间信息': ",".join(房间信息[str].split()), '租房链接': f'https:/sh.lianjia.com{租房URL[str]}',
                        '房间特点': 特点[str], '房间面积': 房间面积[str], '可租房间数量': 数量[str], '房间坐标': 坐标[str],
                        '房间大小': 房间间数[str], "房间地址": 地址_l[str], '租金': f'{金额[str]}{单位[str]}'}
        __lst__.append([",".join(房间信息[str].split()), 房间面积[str], 地址_l[str], 房间间数[str], 坐标[str], 数量[str], f'https:/sh.lianjia.com{租房URL[str]}', 特点[str], f'{金额[str]}{单位[str]}'])
    if sign:
        return __dicts__
    else:
        return __lst__
def 保存数据(date,file_name='租房信息爬取',sign=0):
    with open(f'{file_name}.csv', 'a+', newline='', encoding='utf-8') as f:
        if sign:
            x = 1
            for i in date:
                if len(date[i]) == 9:
                    filednames = ['房间信息', '租房链接', '房间特点', '房间面积', '可租房间数量', '房间坐标', '房间大小', '房间地址', '租金']
                else:
                    filednames = ['房间信息', '房间面积', "房间地址", '房间间数', '房间朝向', '房间层数', '可租数量', '租房链接', '房间状态', '价格']
                x += 1
            writer = csv.DictWriter(f, fieldnames=filednames)
            writer.writeheader()
            for ont in date:
                writer.writerow(date[ont])
        else:
            writer = csv.writer(f)
            writer.writerow(['房间信息', '房间面积', '房间地址', '房间大小', '房间坐标', '可租房间数量', '租房链接', '房间特点', '租金'])
            for one in date:
                writer.writerow(one)

if __name__ == '__main__':
    for v in range(1,10):
        xt = 爬取数据(1)
        # 保存数据(获取数据1(xt, sign=1), sign=1)
        # 保存数据(获取数据1(xt), file_name='租房信息爬取(list)')
        保存数据(获取数据2(xt, sign=1), sign=1)
        保存数据(获取数据2(xt), file_name='租房信息爬取(list)')
