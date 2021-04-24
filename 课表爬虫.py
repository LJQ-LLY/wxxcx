"""
    作者：李俊其
"""

import requests
from bs4 import BeautifulSoup
import re
import pymysql

class Main():

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            # "Cookie": "JSESSIONID=EB1AEE69198E09270A50E1C754EFA2AF; browserID=2807932813"
            "Host": "210.38.250.43"
        }

        self.url = "http://210.38.250.43"
        self.post_url = "http://210.38.250.43/login!doLogin.action"
        # self.kebiao_url = "http://210.38.250.43/xsgrkbcx!getKbRq.action?xnxqdm=202002&zc=8"
        self.data = {
            "account": None,
            "pwd": "bGlqdW5xaS4yMDAzMDEyOA==",
            # "verifycode": ""
        }
        # data = self.data,
        self.zbksj = []
        self.session = requests.Session()

        # self.request()

    def request(self, kebiao_url):
        Response = self.session.get(self.url, headers=self.headers)
        # print(Response.status_code)
        response = self.session.post(self.post_url, headers=self.headers, data=self.data)
        # print(response.status_code)
        res = self.session.get(kebiao_url, headers=self.headers)
        # print(res.status_code)
        # print(res)
        soup = BeautifulSoup(res.text, "lxml")
        # print(soup)
        soup = str(soup)
        model = re.compile("<html>.*<p>(.*)</p>.*</html>", re.S)
        result = re.findall(model, soup)
        x = result
        result = eval(result[0])[0]
        day = eval(x[0])[1]
        # print(day)
        kbsj = []
        for i in result:
            # print(i)
            y = int(i['xq']) - 1
            daytime = day[y]['rq']
            # print(daytime)
            sksj = {
                'kcmc': i['kcmc'],
                'teaxms': i['teaxms'],
                'jxcdmc': i['jxcdmc'],
                'jcdm': i['jcdm'],
                'xq': i['xq'],
                'zc': i['zc'],
                'daytime': daytime
            }
            # print(sksj)
            kbsj.append(sksj)

        self.zbksj.append(kbsj)

    def __getitem__(self, item):
        self.data['account'] = item


class DB():

    def __init__(self, ojb):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='lijunqi.20030128',
                                    database='kebiao')
        self.cur = self.conn.cursor()
        self.ojb = ojb
        self.intosql()

    def intosql(self):
        # xh = self.ojb.data['account']
        for i in self.sjcl():
            # print("%s"%",".join(i))
            sql ='''
                    insert into kbsj
                    (
                        xh,kcmc,teaxms,jxcdmc,jcdm,xq,zc,daytime
                    )values(%s)
            '''%",".join(i)
            # print(sql)
            self.cur.execute(sql)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def sjcl(self):
        for i in range(len(self.ojb.zbksj)):
            week_kb = self.ojb.zbksj[i]
            # print(type(self.ojb.data['account']))
            for x in week_kb:
                str_list = [
                    "'" + str(self.ojb.data['account']) + "'",
                    "'" + x['kcmc'] + "'",
                    "'" + x['teaxms'] + "'",
                    "'" + x['jxcdmc'] + "'",
                    "'" + x['jcdm'] + "'",
                    "'" + x['xq'] + "'",
                    "'" + x['zc'] + "'",
                    "'" + x['daytime'] + "'"
                ]

                yield str_list


if __name__ == '__main__':
    main = Main()
    main[int(input("请输入:"))]
    url = 'http://210.38.250.43/xsgrkbcx!getKbRq.action?xnxqdm=202002&zc='
    for i in range(1, 18):
        kburl = url + str(i)
        main.request(kburl)
    print(main.zbksj)
    db = DB(main)
