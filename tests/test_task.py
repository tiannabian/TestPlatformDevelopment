#coding: utf-8
#author = hewangtong
#date = 2020/9/29
from time import sleep

import requests

from core.backend import jenkins
from tests.base_testcase import BaseTestCase


class TestTask(BaseTestCase):
    def test_task_post(self):
        pre = jenkins['testcase_01'].get_last_build().get_number()
        print(pre)
        r = requests.post(
            'http://127.0.0.1:5000/task',
            headers={'Authorization': f'Bearer {self.token}'},
            json={'testcase': 'sub_dir'}
        )
        for i in range(10):
            if not jenkins['testcase_01'].is_queued_or_running():
                break
            else:
                print('wait')
                sleep(1)
        last = jenkins['testcase_01'].get_last_build().get_number()
        print(last)
        assert last == pre+1


    def test_task_get(self):
        '''获取所有构建任务信息'''
        r = requests.get(
            'http://127.0.0.1:5000/task',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        print(r.json())



