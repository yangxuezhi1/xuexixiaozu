import csv
from re import compile
from json import loads
from requests import get
from time import sleep

number = '000601-2300999'

def get_html(url):
    par = compile('SNB.cubeInfo = ({.*})?;')
    par1 = compile('SNB.cubeTreeData = ({.*})?;')
    headers = {
        'cookie': 'acw_tc=2760823a16013457663648609ea6ffc97fed51d8c45af725758623f0c12d55; xq_a_token=636e3a77b735ce64db9da253b75cbf49b2518316; xqat=636e3a77b735ce64db9da253b75cbf49b2518316; xq_r_token=91c25a6a9038fa2532dd45b2dd9b573a35e28cfd; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYwMjY0MzAyMCwiY3RtIjoxNjAxMzQ1NzMyOTc5LCJjaWQiOiJkOWQwbjRBWnVwIn0.ag9uBSabq7f9l_Uk7qzn_NnSG7KPcPNtTB-4AF4UwObzLPDWR5x8Tji_1d4yU32aifePnY4YVukrOuyWlThJEgx-uNqVU7KtP9QDT6WHZoEhPrpMx5SwHEb2GYLL1p-opNIwAxO7XgplkiMX2eYu7XIRxmmAZtBA7tgRtfPKjAsMDKxWcJr2cM2UkgFMXHLtnz1njDbWWw_2zF7qKk5hrOcwRQPqhx1CREyt3c6fosWj20KVb5dwvDQiG1Gk2vJz8tzk5hgMVftTbKd1gyNEYtSIBpFE1kI0Fp6AcoZNMlfLmwPbwJIVNtuAmOCWt8Tsij_aJz9ySjzzI144JtM3EA; u=731601345766369; Hm_lvt_1db88642e346389874251b5a1eded6e3=1601345769; device_id=24700f9f1986800ab4fcc880530dd0ed; s=ce11ghg5me; __utma=1.1521978181.1601345818.1601345818.1601345818.1; __utmc=1; __utmz=1.1601345818.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=1.55.9.1601346113280; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1601347187',
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 78.0.3904.108Safari / 537.36',
        'Connection': 'close',
        'Host': 'xueqiu.com'
    }
    html_txt = get(url, headers=headers)
    if html_txt.status_code == 200:
        html_txt.encoding = 'utf-8'
        result_txt = par.findall(html_txt.text)
        result_txt1 = par1.findall(html_txt.text)
        return [result_txt[0], result_txt1[0]]
    else:
        return [False,False]
def get_date(date_list):
    组合字典,持仓字典 = date_list
    组合字典 = loads(组合字典)
    持仓字典 = loads(持仓字典)
    组合名字 = 组合字典['name']
    组合代码 = 组合字典['symbol']
    总收益 = 组合字典['total_gain']
    日收益 = 组合字典['daily_gain']
    月收益 = 组合字典['monthly_gain']
    净值 = 组合字典['net_value']
    组合创建者 = 组合字典['owner']['screen_name']
    组合创建者私人网页 = f'https://xueqiu.com/u{组合字典["owner"]["profile"]}'
    组合正常标志 = '正常'
    组合创建时间 = 组合字典['created_date']
    组合关停时间 = ''
    if 组合字典['close_date'] != '':
        组合正常标志 = '已关停'
        组合关停时间 = 组合字典['close_date']
    stock = []
    if 持仓字典 != {}:
        stock2 = []
        stock1 = []
        for i in 持仓字典:
            股票类型 = 持仓字典[i]['name']
            持股比重 = 持仓字典[i]['weight']
            if 'stocks' in 持仓字典[i]:
                for x in 持仓字典[i]['stocks']:
                    stock1.append(','.join([x['stock_name'], f"{x['weight']}", x['stock_symbol'], f"'https://xueqiu.comx['url']"]))
                stock2.append(f"{股票类型},{持股比重},{','.join(stock1)}")
        stock = ','.join(stock2).split(',')
    file_list = [组合名字,组合代码,总收益,日收益,月收益,净值,组合创建者,组合创建者私人网页,组合创建时间,组合正常标志,
                 组合关停时间]+stock
    return file_list

def save_file(date,file_name):
    with open(f'{file_name}.csv', 'a+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(date)

if __name__ == '__main__':

    # pass
    error = 0
    num = int(input('请输入你想爬取到那页的组合结束？（需大于601）'))
    for i in range(601, num):
        while len(str(i)) < 6:
            i = f'0{i}'
        url = f'https://xueqiu.com/P/ZH{i}'
        lst = get_html(url)
        if lst[0] == False and error <50:
            error += 1
            pass
        elif error == 50:
            print('页面错误过多，停止运行')
            break
        else:
            file_name = '雪球组合'
            date = get_date(lst)
            save_file(date,file_name)
            error = 0
        sleep(1)

