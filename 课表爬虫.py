"""
    作者：李俊其
"""

import requests
from bs4 import BeautifulSoup
import re


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
            "account": 20034480324,
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
        result = eval(result[0])[0]
        kbsj = []
        for i in result:
            # print(i)
            sksj = {
                'kcmc': i['kcmc'],
                'teaxms': i['teaxms'],
                'jxcdmc': i['jxcdmc'],
                'jcdm2': i['jcdm2'],
                'xq': i['xq'],
                'zc': i['zc']
            }
            print(sksj)
            kbsj.append(sksj)

        self.zbksj.append(kbsj)


if __name__ == '__main__':
    main = Main()
    url = 'http://210.38.250.43/xsgrkbcx!getKbRq.action?xnxqdm=202002&zc='
    for i in range(1, 18):
        kburl = url + str(i)
        main.request(kburl)

    print(main.zbksj)