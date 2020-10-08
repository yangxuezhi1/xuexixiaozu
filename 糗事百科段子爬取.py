from requests import get
from lxml import etree

headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 78.0.3904.108Safari / 537.36',
        'Connection': 'close'
    }

def get_html(url):
    lst = []
    print(url)
    response = get(url, headers=headers)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    print(html)
    ht_lst = html.xpath('.//div[@class="col1 old-style-col1"]/div')
    for i in ht_lst:
        name = i.xpath('./div[1]//h2/text()')[0].replace('\n', '')
        content = ''.join(i.xpath('./a[1]//span[1]/text()')).replace(' ', '').replace('\n', '').replace('…', '')
        content_url = f'https://www.qiushibaike.com/{i.xpath("./a[1]/@href")[0]}'
        stats_vote = f'共 {i.xpath("./div[2]/span[1]//i/text()")[0]} 好笑'
        stats_comments = f'{i.xpath("./div[2]/span[2]//i/text()")[0]} 评论'
        god_cmt_name = ''
        god_cmt_text = ''
        if i.xpath('./a[2]'):
            god_cmt_name = i.xpath('./a[2]/div/span[2]/text()')[0]
            god_cmt_text = i.xpath('./a[2]/div/div[1]/text()')[0].replace('\n', '')
        lst.append(','.join([name, content, content_url, stats_vote, stats_comments, god_cmt_name, god_cmt_text]))
    if html.xpath('.//span[@class="next"]'):
        print(lst)
        return [lst, True]
    else:
        print(lst)
        return [lst, False]



def save_file(data,file_name):
    with open(file_name, 'a', encoding='utf-8') as f:
        for i in data:
            f.write(i+'\n')


if __name__ == '__main__':
    number = int(input())
    for x in range(1, number+1):
        url = f'https://www.qiushibaike.com/text/page/{x}/'
        lst = get_html(url)
        if lst[1]:
            save_file(lst[0], '糗事百科段子.txt')
        elif not lst[1]:
            save_file(lst[0], '糗事百科段子.txt')
            print(f'目前已为您查到并保存{x}页的段子内容，因{x+1}页无段子内容，现程序停止')
            break
