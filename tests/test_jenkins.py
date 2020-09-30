#coding: utf-8
#author = hewangtong
#date = 2020/9/29
from jenkinsapi.jenkins import Jenkins

def test_jenkins():
    jenkins = Jenkins(
        'http://stuq.ceshiren.com:8020/',
        username='hewangtong',
        password='111d38e8dafde5fe6770149abbd8a90d39'
    )

    jenkins['testcase_01'].invoke(
        securitytoken='111d38e8dafde5fe6770149abbd8a90d39',
        build_params={
            'testcases': '.'
        }
    )

    print(jenkins['testcase_01'].get_last_completed_build().get_console())