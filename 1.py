from json import loads
import csv
from time import sleep

from requests import get
from urllib.request import urlretrieve

headers = {
    'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 78.0.3904.108Safari / 537.36',
    'Connection': 'close'
}

def 任务一():
    url = 'http://t.yushu.im/v2/movie/subject/3'
    js_txt = get(url, headers=headers)
    if js_txt.status_code == 200:
        txt = loads(js_txt.text)
        image_url = txt['images']['large']
        file_title = txt['original_title']
        urlretrieve(image_url, f'{file_title}.jpg') #方法一
    # img_file = get(image_url, headers=headers,stream=True)
    # if img_file.status_code == 200:
    #      with open(f'{file_title}.jpg', 'wb') as f:
    #         for c in img_file.iter_content(chunk_size=1024):    #方法二
    #             f.write(c)
    # #         f.write(img_file.content)    #方法三
    print('Pass')



def 任务二(city,file_name,size='a+',encod='utf-8',newl=''):
    海报图片 = {}
    params = {
        'start': city
    }
    f_csv_lst = ['电影序号', '电影标题', '电影评分', '电影分类', '导演名字', '电影主演', '电影海报URL']
    with open(file_name, size, encoding=encod, newline=newl) as f:
        f_csv = csv.writer(f)
        if city == 0:
            f_csv.writerow(f_csv_lst)
    url = 'http://t.yushu.im/v2/movie/top250'
    js_txt = get(url, params=params, headers=headers)
    if js_txt.status_code == 200:
        txt = loads(js_txt.text)
        subjects = txt['subjects']
        for data in subjects:
            电影序号 = data['comments_count']
            导演名字 = data['directors'][0]['name']
            电影标题 = data['title']
            电影评分 = data['rating']['average']
            电影分类 = ','.join(data['genres'])
            电影海报URL = data['images']['large']
            lst = data['casts']
            电影主演 = ','.join([i['name'] for i in lst])
            海报图片[电影序号] = 电影海报URL
            with open(file_name, size, encoding=encod, newline=newl) as f:
                f_csv = csv.writer(f)
                f_csv.writerow([电影序号, 电影标题, 电影评分, 电影分类, 导演名字, 电影主演, 电影海报URL])
    return 海报图片

def 任务三(item):
    """
    :param item: 字典格式文件
    :return:
    """
    for k,v in item.items():
        img_file = get(v, headers=headers, stream=True)
        if img_file.status_code == 200:
            with open(f'D:\\Python Files\\Pythonobj\\学习小组\\任务二\\images\\{k}.jpg', 'wb') as f:
                for c in img_file.iter_content(chunk_size=1024):    #方法二
                    f.write(c)
        sleep(0.5)


if __name__ == '__main__':
    for i in range(13):
        it = 任务二(i*20, 'top250.csv')
        任务三(it)
    print('pass!')