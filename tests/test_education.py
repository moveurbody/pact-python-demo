# -*- coding: utf-8 -*-
# @Time    : 2019/12/26 上午11:35
# @Author  : yu_hsuan_chen@trendmicro.com
# @File    : test_education
# @Version : 3.6

import os

import pytest
import requests
from pact import EachLike, SomethingLike
from pact.consumer import Consumer
from pact.provider import Provider

from pact_python_demo.client import UserClient

PACT_MOCK_HOST = '127.0.0.1'
PACT_MOCK_PORT_TEACHER = 8001
PACT_MOCK_PORT_STUDENT = 8002
PACT_DIR = os.path.dirname(os.path.realpath(__file__))
print(PACT_DIR)


@pytest.fixture
def client():
    return UserClient('http://{host}:{port}'.format(host=PACT_MOCK_HOST, port=PACT_MOCK_PORT_STUDENT))


@pytest.fixture(scope='session')
def pact_student():
    pact = Consumer('EducationService').has_pact_with(
        Provider('StudentInfoService'),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT_STUDENT,
        pact_dir=PACT_DIR)
    pact.start_service()
    yield pact
    pact.stop_service()


@pytest.fixture(scope='session')
def pact_teacher():
    pact = Consumer('EducationService').has_pact_with(
        Provider('TeacherInfoService'),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT_TEACHER,
        pact_dir=PACT_DIR)
    pact.start_service()
    yield pact
    pact.stop_service()


def test_student(pact_student):
    print("test student")
    request_url = 'http://127.0.0.1:8002/api/students/'

    expected = EachLike({
        'id': SomethingLike(1),
        'name': SomethingLike('Eric'),
        'class': EachLike('English'),
        'age': SomethingLike(10)
    })

    (pact_student.given('a simple json blob exists')
     .upon_receiving('a query for the user Jonas')
     .with_request(method='GET', path='/api/students/')
     .will_respond_with(200, body=expected))

    with pact_student:
        results = requests.get(request_url)


def test_get_all_teachers(pact_teacher):
    request_url = 'http://127.0.0.1:8001/api/teachers/'

    expected = EachLike({
        'id': SomethingLike(1),
        'name': SomethingLike("Doris Wilson"),
        'class': EachLike(('TILLETT')),
    })

    (pact_teacher.given('some teachers information exist')
     .upon_receiving('a query for all teacher information')
     .with_request(method='GET', path='/api/teachers/')
     .will_respond_with(200, body=expected))

    with pact_teacher:
        results = requests.get(request_url)


def test_get_exist_teacher_information_by_id(pact_teacher):
    request_url = 'http://127.0.0.1:8001/api/teachers/1'

    expected = SomethingLike({
        'id': SomethingLike(1),
        'name': SomethingLike("Doris Wilson"),
        'class': EachLike(('TILLETT')),
    })

    (pact_teacher.given('teacher id is existed')
     .upon_receiving('a query for teacher id 1')
     .with_request(method='GET', path='/api/teachers/1')
     .will_respond_with(200, body=expected))

    with pact_teacher:
        results = requests.get(request_url)


def test_get_non_exist_teacher_information_by_id(pact_teacher):
    request_url = 'http://127.0.0.1:8001/api/teachers/3'

    expected = {}

    (pact_teacher.given('teacher id is not existed')
     .upon_receiving('a query for teacher id 3')
     .with_request(method='GET', path='/api/teachers/3')
     .will_respond_with(500, body=expected))

    with pact_teacher:
        results = requests.get(request_url)
