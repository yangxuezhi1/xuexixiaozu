import csv
import requests
import os,re
import json
import time

class get_railway_ticket_quantity(object):
    mon_lst = [m for m in range(1,13)]
    day_lst = [d for d in range(1,31)]
    year, mon, day = [0, 0, 0]
    lst = ''
    def __init__(self):
        self.url = 'https://kyfw.12306.cn/otn/leftTicket/query'
        self.station_lst = []
        self.st_lst = []
        self.time_s = time.localtime(time.time())
        self.file_path = os.getcwd()
        self.station_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
        self.st_lst_path = self.file_path+'\\CSV\\station list.csv'
        self.headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 78.0.3904.108Safari / 537.36',
            'Connection': 'close',
        }
        self.params = {
            'leftTicketDTO.train_date': '2020-10-02',
            'leftTicketDTO.from_station': 'AKY',
            'leftTicketDTO.to_station': 'AOH',
            'purpose_codes': 'ADULT'
        }

    def check_file_exists(self):
        if os.path.exists(self.file_path+'\\CSV'):
            if os.path.isfile(self.st_lst_path):
                self.load_st_lst()
            else:
                self.get_station_lst()
                self.save_station_lst()
                self.check_file_exists()
        else:
            os.mkdir(self.file_path+'\\CSV')
            self.get_station_lst()
            self.save_station_lst()
            self.check_file_exists()

    def get_station_lst(self):
        response = requests.get(self.station_url)
        response.encoding = 'utf-8'
        station_lst = response.text.split('=')[1].split('@')
        self.station_lst = [i.split('|')[1:-1] for i in station_lst if i != '']

    def load_st_lst(self):
        with open(self.st_lst_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for i in reader:
                if i:
                    self.st_lst.append(i[:2])

    def save_station_lst(self):
        with open(self.st_lst_path, 'w', newline='', encoding='utf-8') as f:
            write = csv.writer(f)
            write.writerows(self.station_lst)

    def y_m_d_judgment(self, y, m, d):
        while True:
            if y == self.year and ((m == self.mon or m == self.mon+1)and m in self.mon_lst) and \
                ((m == self.mon and d in self.day_lst and d >= self.day)or
                 (m == self.mon+1 and d in self.day_lst and d <= self.day)):
                if len(str(m)) < 2:
                    m = f'0{m}'
                if len(str(d)) < 2:
                    d = f'0{d}'
                return f'{y}-{m}-{d}'
            else:
                query_day = input('ERROR:输入的日期参数不在查询范围内，请重新输入')
                y, m, d = self.ste_split(query_day)
                continue

    def ste_split(self, query_day):
        while True:
            try:
                lst = [int(i) for i in query_day.split('-')]
            except ValueError:
                query_day = input('ERROR:输入的日期参数存在非数字或未使用‘-’分隔，请重新输入')
            else:
                return lst

    def data_filter(self, name):
        n_l = []
        for i in self.st_lst:
            if name in i[0]:
                n_l.append(i)
        return n_l

    def prinat_station(self, lst, size='乘车'):
        str1 = f'请从下列车站中找到你需要{size}的车站，如存在两个，选择前面的那个\n 序号 \t 车站名'
        print(str1)
        if size:
            for i in range(len(lst)):
                print(f' {i+1} \t  {lst[i][0]}')
        else:
            for i in lst:
                print(i)
        number = input('请输入您需要乘车的车站对应的序号，谢谢')
        while True:
            try:
                number = int(number)-1
            except ValueError:
                number = input('ERROR:输入的内容存在非数字字符，请重新输入!')
            else:
                return lst[number][1]

    def Get_Ticket_Information(self, tiem, fro, to):
        self.params['leftTicketDTO.train_date'] = tiem
        self.params['leftTicketDTO.from_station'] = fro
        self.params['leftTicketDTO.to_station'] = to
        self.headers['cookie'] = '_uab_collina=160153499209807069222547; JSESSIONID=9EBC15785AD52BFE3F4814B4C65C5ADA; RAIL_EXPIRATION=1601854054075; RAIL_DEVICEID=IcQgD4pCzq8fJ_lpsXcgE7ZLjdp66oEVJz9BgVd-acPYHXMrRLigkuTIcMacH-6i714KVnDdGLvVkp1uT4HKxshUA7eZyMMZErMiCSjN2oFw3C487v_X_kgcnC0SuEenMhA7HI9PBcJltqi2731PqdDgkpM2fGt9; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5E7F%u5DDE%2CGZQ; _jc_save_toStation=%u6DF1%u5733%2CSZQ; _jc_save_fromDate=2020-10-17; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=66060810.24610.0000; _jc_save_toDate=2020-10-03'
        response = requests.get(self.url, params=self.params, headers=self.headers)
        if response.status_code == 200:
            print(response.text)
            try:
                dic = json.loads(response.text)
            except json.decoder.JSONDecodeError:
                raise Exception('cookie异常')#cookie异常，进尽快进行检查或更换
            else:
                if dic['data']['result']:
                    return dic['data']['result']
                else:
                    return False

    def ticket_check(self, train, train_lst):
        if train[0] == 'G':
            商务座 = train_lst[1]
            一等座 = train_lst[2]
            二等座 = train_lst[3]
            return {'车次类型': '高铁', '商务座': 商务座, '一等座': 一等座, '二等座': 二等座}
        elif train[0] == 'D':
            二等座 = train_lst[3]
            软卧 = train_lst[-4]
            硬卧 = train_lst[5]
            无座 = train_lst[7]
            return {'车次类型': '动车', '二等座': 二等座, '软卧': 软卧, '硬卧': 硬卧, '无座': 无座}
        elif train[0] == 'Z':
            高级软卧 = train_lst[-2]
            软卧 = train_lst[-4]
            硬卧 = train_lst[5]
            硬座 = train_lst[4]
            无座 = train_lst[7]
            return{'车次类型': '直达列车', '高级软卧': 高级软卧, '软卧': 软卧, '硬卧': 硬卧, '硬座': 硬座, '无座': 无座}
        elif train[0] == 'T':
            高级软卧 = train_lst[-2]
            软卧 = train_lst[-4]
            硬卧 = train_lst[5]
            硬座 = train_lst[4]
            无座 = train_lst[7]
            return {'车次类型': '特快列车', '高级软卧': 高级软卧, '软卧': 软卧, '硬卧': 硬卧, '硬座': 硬座, '无座': 无座}
        elif train[0] == 'K':
            高级软卧 = train_lst[-2]
            软卧 = train_lst[-4]
            硬卧 = train_lst[5]
            硬座 = train_lst[4]
            无座 = train_lst[7]
            return {'车次类型': '快速列车', '高级软卧': 高级软卧, '软卧': 软卧, '硬卧': 硬卧, '硬座': 硬座, '无座': 无座}
        elif train[0] == 'C':
            一等座 = train_lst[2]
            二等座 = train_lst[3]
            无座 = train_lst[7]
            return {'车次类型': '城际列车', '一等座': 一等座, '二等座': 二等座, '无座': 无座}
        else:
            高级软卧 = train_lst[-2]
            软卧 = train_lst[-4]
            硬卧 = train_lst[5]
            硬座 = train_lst[4]
            无座 = train_lst[7]
            return {'车次类型': '数字车次', '高级软卧': 高级软卧,  '软卧': 软卧, '硬卧': 硬卧, '硬座': 硬座, '无座': 无座}

    def get_input(self):
        query_day = input('请输入您需要查询车票的日期。注：本软件不支持往前查询及不支持30日之后的日期查询，默认为今天。'
                          f'查询日期格式：({self.year}-{self.mon}-{self.day})')
        if query_day != '':
            self.lst = self.ste_split(query_day)
            query_day_s = self.y_m_d_judgment(self.lst[0], self.lst[1], self.lst[2])
        else:
            query_day_s = self.y_m_d_judgment(self.year, self.mon, self.day)
        from_station = input('请输入您需要乘车的车站名。(例：北京站/天津站)')
        if from_station[-1] == '站':
            from_station = from_station[:-1]
        from_ls = self.data_filter(from_station)
        from_s = self.prinat_station(from_ls)
        to_station = input('请输入您需要去往的车站名。(例：上海站/南昌站)')
        if to_station[-1] == '站':
            to_station = to_station[:-1]
        to_ls = self.data_filter(to_station)
        to_s = self.prinat_station(to_ls)
        return [query_day_s, from_s, to_s, from_station, to_station]

    def get_train(self, query_day_s, from_s, to_s):
        lst = self.Get_Ticket_Information(query_day_s, from_s, to_s)
        车票详情 = {}
        if lst:
            for i in lst:
                i1 = i.split('|')
                sign = i1[11]
                train = i1[3]
                train_lst = i1[20:34]
                train_lst.reverse()
                if sign != 'IS_TIME_NOT_BUY':
                    t_r_l = self.ticket_check(train, train_lst)
                    车票详情[train] = {'train': train, 'sign': sign, 'train_lst': t_r_l}
                else:
                    车票详情[train] = {'train': train, 'sign': '列车暂停发售', 'train_lst': {}}
            return 车票详情
        else:
            return ''

    def get_check_train(self, train, from_station, to_station, train_s=''):
            if train_s != '':
                while True:
                    if train_s in train.keys():
                        print(f"车次：{train[train_s]['train']},  可否订票：{train[train_s]['sign']}，详细车票数量：")
                        for k, v in train[train_s]['train_lst'].items():
                            if v == '':
                                v = '无'
                            try:
                                v = int(v)
                            except ValueError:
                                pass
                            else:
                                v = f'剩余{v}张'
                            print(f'{k}：{v}')
                        break
                    else:
                        print('您输入的车次暂未查询到或您查询的车次已经发车，请您换趟车次查询，谢谢')
                        train_s = input('请输入您需要查询的车次')
            else:
                print(f'抱歉，按您的查询条件，当前未找到从{from_station}到{to_station} 的列车')

    def get_sleep_time(self, tiem, train, from_station,  to_station, train_s, stop_sign):
        while stop_sign:
            self.get_check_train(train, from_station, to_station, train_s=train_s)
            time.sleep(float(tiem)*60)
            stop_sign -= 1

    def app(self):
        stop_sign = 1
        sleep_t = 0.00
        """主运行函数"""
        self.check_file_exists()
        self.year, self.mon, self.day = self.time_s[0], self.time_s[1], self.time_s[2]
        query_day_s, from_s, to_s, from_station, to_station = self.get_input()
        train = self.get_train(query_day_s, from_s, to_s)
        if train != '':
            print(f'目前查询到了{len(train)}趟从{from_station}开往{to_station}的列车,分别是：')
            for i in train:
                print(f'{train[i]["train"]}  次，', end='')
            print()
        train_s = input('请输入您需要查询的车次')
        sign = input('请问您需要定时为您查询车票余量吗？（y/n）')
        if sign.lower() == 'y':
            sleep_t = float(input('您计划多少时间查询一次（分钟）'))
            stop_sign = int(input('您计划查询多少次'))
        self.get_sleep_time(sleep_t, train, from_station,  to_station, train_s, stop_sign)

a1 = get_railway_ticket_quantity()
a1.app()


