#coding: utf-8
#author = hewangtong
#date = 2020/9/20
import datetime
import pytest
import  requests
from tests.base_testcase import BaseTestCase

class TestCase(BaseTestCase):
    def test_add(self):
        """
        测试添加用例
        :return:
        """
        r = requests.post(
            'http://127.0.0.1:5000/testcase',
            headers={'Authorization': f'Bearer {self.token}'},
            json = {
                'name': f'name{str(datetime.datetime.now())}',
                'description': 'd',
                'data': ''
            }
        )
        assert r.status_code == 200
        assert r.json()['msg'] == 'ok'

    def test_put(self):
        """
        测试用例编辑
        :return:
        """
        name = 'heyang'
        description = '这里测试一下'
        update_name = 'updateheyang'
        update_description = '更新这里测试一下'
        update_data = 'updatedata'
        r = requests.put(
            'http://127.0.0.1:5000/testcase',
            headers={'Authorization': f'Bearer {self.token}'},
            json={
                'name': name,
                'description': description,
                'update_name': update_name,
                'update_description': update_description,
                'update_data': update_data
            }
        )
        print(r.json())
        assert r.status_code == 200

    def test_delete(self):
        """
        测试测试用例删除
        :return:
        """
        name = 'join'
        description = '120'
        r = requests.delete(
            'http://127.0.0.1:5000/testcase',
            headers={'Authorization': f'Bearer {self.token}'},
            json={
                'name': name,
                'description': description
            }
        )
        print(r.json())
        assert r.status_code == 200