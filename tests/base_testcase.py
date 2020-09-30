#coding: utf-8
#author = hewangtong
#date = 2020/9/29
import requests


class BaseTestCase:
    def setup_class(self):
        username = 'heyang'
        password = 'p@ssw0rd'
        r = requests.post(
            'http://127.0.0.1:5000/login',
            json={
                'username': username,
                'password': password
            }
        )
        self.token = r.json()['token']