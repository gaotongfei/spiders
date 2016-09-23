import requests
from bs4 import BeautifulSoup
from getpass import getpass
# python3
try:
    import http.cookiejar as cookielib
    from http.cookiejar import LoadError
# python2
except:
    import cookielib
    from cookielib import LoadError
    input = raw_input


class Douban:
    """
    使用:

    1. 命令行
        $ python douban.py
            密码: *******
            请到当前目录找到captcha文件, 并输入验证码
            captcha
        $ douban.scrape_doumail()
        $ douban.do_other_stuff()
    2. from douban import Douban

       douban = Douban()
       douban.login('<yourusername>', '<yourpassword>')
       douban.scrape_doumail()
       douban.do_other_stuff()
    """
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6,zh-TW;q=0.4'
        }
        self.session = requests.session()

        # 首先创建名为cookies空文件
        open('cookies', 'a').close()
        # 加载cookies
        self.session.cookies = cookielib.LWPCookieJar(filename='cookies')

        try:
            self.session.cookies.load(ignore_discard=True)
        except LoadError:
            pass

        self.url = 'https://www.douban.com/login'
        self.response = self.session.get(self.url, headers=self.headers)

        try:
            self.soup = BeautifulSoup(self.response.text, "lxml")
        except:
            self.soup = BeautifulSoup(self.response.text, "html.parser")

    def _get_captcha_id(self):
        return self.soup.find("input", {"name": "captcha-id"}).get('value')

    def get_captcha(self):
        captcha_id = self._get_captcha_id()
        captcha_url = 'https://www.douban.com/misc/captcha?id={0}&size=s'.format(captcha_id)
        r = self.session.get(captcha_url)
        with open('captcha', 'wb') as f:
            f.write(r.content)

        print("请到当前目录找到captcha文件, 并输入验证码")
        captcha = input()
        return captcha, captcha_id

    def login(self, username, password=None):
        if not password:
            password = getpass(prompt='密码:')

        captcha, captcha_id = self.get_captcha()

        form_data = {
            'source': None,
            'redir': 'https://www.douban.com',
            'form_email': username,
            'form_password': password,
            'captcha-solution': captcha,
            'captcha-id': captcha_id,
            'login': '登录'
        }
        response = self.session.post(self.url, data=form_data, headers=self.headers)
        self.session.cookies.save()

    # 爬爬豆邮, 看看那些人给你发过豆邮
    def scrape_doumail(self):
        url = 'https://www.douban.com/doumail/'
        response = self.session.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, "lxml")
        print([s.text for s in soup.select('.from')])

    def do_other_stuff(self):
        pass

if __name__ == '__main__':
    douban = Douban()
    douban.login('gaotongfei1995@gmail.com')
    douban.scrape_doumail()
