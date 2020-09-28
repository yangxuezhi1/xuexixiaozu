import csv
from requests import get
from lxml import etree

url = 'https://www.liepin.com/zhaopin/'
params = {
    'key': 'python',
    'curPage': 0
}
headers = {
    'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 78.0.3904.108Safari / 537.36',
    'Connection': 'close'
}
def writer(date, size=False):
    with open('招聘信息.csv', 'a+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if size == False:
            writer.writerow(['招聘职位', '工资', 'URL', '应聘前提', '公司福利', '工作地点', '工作职责',
                             '任职资格', '公司名称','公司简介', '公司详情', '招聘信息更新时间'])
        writer.writerow(date)
def ger_date():
    size = False
    response = get(url, params=params, headers=headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    nums = html.xpath('.//a[@class="last"]/@href')[0].split('curPage=')[-1]
    for num in range(nums+1):
        params['curPage'] = num
        response = get(url, params=params, headers=headers)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        二级标签 = html.xpath('//div[@class ="job-info"]/h3/a/@href')
        更新时间 = html.xpath('//p[@class="time-info clearfix"]/time/text()')
        二级URL = []
        for i in 二级标签:
            二级URL.append(i.split('?')[0])
        for i in range(len(二级URL)):
            erjihtml = get(二级URL[i],headers=headers)
            erjihtml.encoding = 'utf-8'
            html = etree.HTML(erjihtml.text)
            main_html = html.xpath('.//div[@class="clearfix"]/div[@class="main "]')[0]
            side_html = html.xpath('.//div[@class="clearfix"]/div[@class="side"]')[0]
            招聘职位 = main_html.xpath('.//div[@class="title-info"]/h1/@title')[0]
            工资 = main_html.xpath('.//div[@class="job-title-left"]/p[1]/text()')[0].replace(' ', '').replace('\r\n', '')
            工作区域 = main_html.xpath('.//div[@class="job-title-left"]/p[last()]/span/a/text()')[0]
            应聘前提 = ','.join(main_html.xpath('.//div[@class="job-qualifications"]/span/text()'))
            公司福利 = ','.join(main_html.xpath('.//div[@class="comp-tag-box"]/ul/li/span/text()'))
            工作职责 = main_html.xpath('.//div[@class="content content-word"]/text()')
            公司名称 = side_html.xpath('.//div[@class="company-logo"]/p/a/text()')[0]
            公司简介 = ','.join(side_html.xpath('.//ul[@class="new-compintro"]/li/text()'))
            公司详情 = ','.join(side_html.xpath('.//ul[@class="new-compdetail"]/li[position()<5]/text()'))
            size1 = 0
            size2 = len(工作职责)
            for x in 工作职责:
                if '岗位' in x:
                    size1 = 工作职责.index(x)
                if '任职'in x:
                    size2 = 工作职责.index(x)
            工作职责1 = ','.join(工作职责[size1:size2])
            任职资格 = ','.join(工作职责[size2:len(工作职责)]).replace(' ', '').replace('\r\n', '')
            writer([招聘职位, 工资, 二级URL[i], 应聘前提, 公司福利, 工作区域, 工作职责1,
                            任职资格, 公司名称, 公司简介, 公司详情, 更新时间[i]], size)
            size = True
if __name__ == '__main__':
    ger_date()
