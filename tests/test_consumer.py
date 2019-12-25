# -*- coding: utf-8 -*-
# @Time    : 2019/12/25 下午4:08
# @Author  : yu_hsuan_chen@trendmicro.com
# @File    : test_consumer
# @Version : 3.6

import atexit
import os
import unittest

import requests
from pact import EachLike, SomethingLike
from pact.consumer import Consumer
from pact.provider import Provider

PACT_MOCK_HOST = 'localhost'
PACT_MOCK_PORT = 8002
PACT_DIR = os.path.dirname(os.path.realpath(__file__))

pact = Consumer('consumer').has_pact_with(Provider('provider'), host_name=PACT_MOCK_HOST, port=PACT_MOCK_PORT)
pact.start_service()
atexit.register(pact.stop_service)


class TestCases(unittest.TestCase):
    def test_student(self):
        request_url = 'http://127.0.0.1:8002/api/students/'

        expected = EachLike({
                'id': SomethingLike(1),
                'name': SomethingLike('Eric'),
                'class': EachLike('English'),
                'age': SomethingLike(10)
            })

        (pact.given('a simple json blob exists')
         .upon_receiving('a query for the user Jonas')
         .with_request(method='GET', path='/api/students/')
         .will_respond_with(200, body=expected))

        with pact:
            results = requests.get(request_url)

        self.assertTrue(results.status_code == 200)
