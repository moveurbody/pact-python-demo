# -*- coding: utf-8 -*-
# @Time    : 2019/12/24 下午3:43
# @Author  : yu_hsuan_chen@trendmicro.com
# @File    : people
# @Version : 3.6

from flask import Flask, abort, jsonify, request
from flasgger import Swagger

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True, port=1000)