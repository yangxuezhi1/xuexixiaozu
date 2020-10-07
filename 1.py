from tools import Base64_Encryption as BE
from requests import get
from lxml import etree
from json import loads
import time


headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 78.0.3904.108Safari / 537.36',
        'Connection': 'close'
    }
name = []
id = []
content = []
agree = []
refuse = []
tucao_lst = []
def get_qa_html(url):
    print(f'GET {url} ing')
    html_res = get(url, headers=headers)
    html_res.encoding = 'utf-8'
    html = etree.HTML(html_res.text)
    li_lst = html.xpath('//ol[@class="commentlist"]/li')
    for i in li_lst:
        name.append(i.xpath('./div/div/div[1]/strong/text()')[0])
        id.append(str(i.xpath('./div/div/div[2]/span/a/text()')[0]))
        content.append(i.xpath('./div/div/div[2]/p/text()')[0])
        agree.append(i.xpath('./div/div/div[3]/span[2]/span/text()')[0])
        refuse.append(i.xpath('./div/div/div[3]/span[3]/span/text()')[0])
    url0 = html.xpath('.//a[@title="Newer Comments"]/@href')
    if url0 != []:
        url0 = url0[0].split('#')[0]
        return f'https:{url0}'
    else:
        return ''

def get_secondary_label(url):
    tucao = []
    res_text = get(url, headers=headers)
    js_tx = loads(res_text.text)
    for i in js_tx['tucao']:
        tucao.append(','.join([i['comment_author'], i['comment_content'].replace('\n', '')]))
    print(tucao)
    return tucao

def app():
    now_time = time.localtime(time.time())
    day = time.strftime('%Y%m%d', now_time)
    url = 'https://jandan.net/qa/' + BE(f'{day}-1')
    while True:
        url = get_qa_html(url)
        time.sleep(0.5)
        if url != '':
            pass
        else:
            break
    print(len(name), len(id), len(content), len(agree), len(refuse))
    for i in range(len(id)):
        url1 = f'https://jandan.net/api/tucao/list/{id[i]}'
        tucao_lst.append(list(get_secondary_label(url1)))
        time.sleep(0.5)
    for i in range(len(id)):
        print(f'{name[i]},{id[i]},{content[i]},{agree[i]},{refuse[i]},{tucao_lst[i]}')

if __name__ == '__main__':
    app()