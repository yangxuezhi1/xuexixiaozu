from requests import get
def 微博热点抓取():
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 78.0.3904.108Safari / 537.36',
        'Connection': 'close'
    }
    url = 'https://weibo.com/a/hot/realtime'
    cookies = 'login_sid_t=3ac3cc75cedcb8b780fe2742cd920199; cross_origin_proto=SSL;' \
              ' YF-V5-G0=b1b8bc404aec69668ba2d36ae39dd980; wb_view_log=1920*10801; _s_tentry=passport.' \
              'weibo.com; Apache=3296740224298.1226.1600998092003; SINAGLOBAL=3296740224298.1226.' \
              '1600998092003; ULV=1600998092180:1:1:1:3296740224298.1226.1600998092003:; ' \
              'crossidccode=CODE-yf-1KlCK2-3HNUDY-gD97lt4pQCrBnL2e426b1; Ugrow-G0=6fd5dedc9d0f894fec342' \
              'd051b79679e; wb_view_log_6734545161=1920*10801; UOR=,,login.sina.com.cn; appkey=; ' \
              'wb_view_log_7506620740=1920*10801; WBtopGlobal_register_version=434eed67f50005bd; ' \
              'ALF=1632534413; SSOLoginState=1600998413; SUB=_2A25yaTxADeRhGeFL61QX8i7LzzyIHXVRHyqI' \
              'rDV8PUNbmtAKLUb2kW9NQoYvHTOOzrOo4Sh11HnreY-u-AY81vFM; SUBP=0033WrSXqPxfM725Ws9jqgMF5' \
              '5529P9D9WFw4jZuyYfUGBHWpNosg1_M5JpX5KzhUgL.FoMfehqceo5NSh52dJLoIEeLxKqL1-BLBKnLxK-LB-' \
              'BLBKqLxKBLBo.L12zp1K.RehME15tt; SUHB=0RyamNPD1CI3eC; wvr=6; YF-Page-G0=112e41ab9e0875' \
              'e1b6850404cae8fa0e|1600998421|1600998160; webim_unReadCount=%7B%22time%22%3A160099860' \
              '2698%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22' \
              '%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; WBStorage=202009250950|undefined'
    headers['cookie'] = cookies
    # headers['host'] = 'https://www.baidu.com'      #来源域名
    # headers['referer'] = 'https://www.baidu.com'   #来源页面
    try:
        res_html = get(url,headers= headers)
    except:
        print('请求错误')
    if res_html.status_code == 200:
        with open('微博热点.html','a+', encoding='utf-8') as f:
            f.write(res_html.text)



if __name__ == '__main__':
    微博热点抓取()
