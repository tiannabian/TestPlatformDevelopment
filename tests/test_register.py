#coding: utf-8
#author = hewangtong
#date = 2020/9/30
import requests
class TestRegister():

    def test_register(self):
        username = 'luxi'
        password = '123456'
        email = '1442678679@qq.com'
        r = requests.post(
            'http://127.0.0.1:5000/register',
            json={
                'username': username,
                'password': password,
                'email': email
            }
        )
        print(r.json())
        assert r.json()['errmsg'] == '注册成功'
