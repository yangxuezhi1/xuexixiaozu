import time
import csv
import requests
from json import loads

headers = {}
headers[
    'User-Agent'] = 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 78.0.3904.108Safari / 537.36'
headers['Connection'] = 'close'
headers['cookie'] = 'q_c1=d71e8c5adf8c49f9abe7cbadfaf31cd0|1601001179000|1601001179000; _zap=0df02087-60f6-42c9-a5be-dfadbdb85403; _xsrf=Ec2LFI56y90OegiBfCET2ZmKUR2ELc4L; d_c0="ACAX22Ha8BGPTuCQ-XR2wUMBcEgFuejEzHs=|1601001151"; capsion_ticket="2|1:0|10:1601001151|14:capsion_ticket|44:ZjUwYzI3YjQzNmZhNDMwZWIwMWM4ZmU2OWUxMzdmMDc=|fc44d1bd4ed7f7a70d2e2c57123ed805458fe51feb4d00d58c0397406a177e28"; _ga=GA1.2.484920414.1601001153; _gid=GA1.2.657252475.1601001153; z_c0="2|1:0|10:1601001178|4:z_c0|92:Mi4xLTVNRER3QUFBQUFBSUJmYllkcndFU1lBQUFCZ0FsVk4ycVJhWUFDdm9pdVZfYTVDekFzNndzcG5BMUN4d3pzR0J3|e5fdc9078fb795bcb80bf507bf810d08aeb5a7e9dd83cf120299866e68fe6f8e"; q_c1=c82ce2c8694a4a6b9256073f132f6b96|1601001378000|1601001378000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1601001152,1601016308; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1601016308; _gat_gtag_UA_149949619_1=1; SESSIONID=JLtOmQKGdnowFuuRZmVWljNY8O34nKJDundItx7eaVt; JOID=VV8QC0le4Hn337g3blEV5767bcJ9FK4AsrfpfiQ_jhSNk8hCPql-E6faujhpgF8-gPU-Ykf3KHkUelvkeMJ4F2M=; osd=V1kSC0pc5nv33LoxbFEW5bi5bcF_EqwAsbXvfCQ8jBKPk8tAOKt-EKXcuDhqglk8gPY8ZEX3K3sSeFvnesR6F2A=; tshl=; tst=r; KLBRSID=4843ceb2c0de43091e0ff7c22eadca8c|1601016336|1601016284'
params = {}
params['session_token'] = '42eba853728c00aa4ae84562baa569d6'
params['desktop'] = 'true'
params['page_number'] = 1
params['limit'] = 6
params['action'] = 'down'
params['after_id'] = 0
params['ad_interval'] = -1
dicts = []
for n in range(5):
    params['limit'] = n+1
    params['after_id'] = n*6
    res = requests.get('https://www.zhihu.com/api/v3/feed/topstory/recommend', params=params, headers=headers)
    dic = loads(res.text)
    for i in dic['data']:
        if i['verb'] == 'TOPIC_ACKNOWLEDGED_ANSWER':
            文章ID = i['id'].split('_')[0]
            times = time.localtime(i['updated_time'])
            更新时间 = time.strftime('%Y--%m--%d %H:%M:%S', times)
            文章作者 = i['target']['author']['name']
            作者链接 = f'https://www.zhihu.com/{i["target"]["author"]["type"]}/{i["target"]["author"]["id"]}'
            作者的话 = i['target']['author']['headline']
            if 'followers_count' in i['target']['author']:
                作者粉丝数 = i['target']['author']['followers_count']
            else:
                作者粉丝数 = 0
            文章评论数 = i['target']['comment_count']
            文章赞同数 = i['target']['voteup_count']
            文章标题 = i['target']['question']['title']
            文章简介 = i['target']['excerpt_new']
            文章类型 = i['action_text']
            附加信息 = i['attached_info']
            print({'文章ID': 文章ID,
            '更新时间': 更新时间,
            '文章作者': 文章作者,
            '作者链接': 作者链接,
            '作者的话': 作者的话,
            '作者粉丝数': 作者粉丝数,
            '文章评论数': 文章评论数,
            '文章赞同数': 文章赞同数,
            '文章标题': 文章标题,
            '文章简介': 文章简介,
            '文章类型': 文章类型,
            '附加信息': 附加信息
            })
            dicts.append({'文章ID': 文章ID,
            '更新时间': 更新时间,
            '文章作者': 文章作者,
            '作者链接': 作者链接,
            '作者的话': 作者的话,
            '作者粉丝数': 作者粉丝数,
            '文章评论数': 文章评论数,
            '文章赞同数': 文章赞同数,
            '文章标题': 文章标题,
            '文章简介': 文章简介,
            '文章类型': 文章类型,
            '附加信息': 附加信息
            })

print(dicts)
with open('zhihu.csv','w',newline='',encoding='utf-8')as f:
    filednames = ['文章ID','更新时间','文章作者','作者链接','作者的话','作者粉丝数',
                  '文章评论数','文章赞同数','文章标题','文章简介','文章类型','附加信息']
    writer = csv.DictWriter(f, fieldnames=filednames)
    writer.writeheader()
    for h in dicts:
        writer.writerow(h)




