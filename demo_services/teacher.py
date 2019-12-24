#!/usr/env/bin python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/24 下午3:42
# @Author  : yu_hsuan_chen@trendmicro.com
# @File    : teacher
# @Version : 3.6

import json

from flasgger import Swagger
from flask import Flask, jsonify

app = Flask(__name__)
Swagger(app)


@app.route('/api/teachers/', methods=['GET'])
def teachers():
    """
    Use the API to get all teachers information
    ---
    tags:
      - Get all teachers information
    responses:
      500:
        description: Fail to get all teachers information
      200:
        description: Get all teachers information
        schema:
          type: array
          items:
            $ref: "#/definitions/teacher_information"
    """
    with open("teacher.json", "r") as json_file:
        teachers_data = json.load(json_file)

    return jsonify(teachers_data), 200


@app.route('/api/teachers/<int:teacher_id>', methods=['GET'])
def teacher(teacher_id):
    """
    Use the API to get teacher's information by id
    ---
    tags:
      - Get all teachers information
    parameters:
      - name: teacher_id
        in: path
        type: integer
        required: true
        description: teacher id
    responses:
      500:
        description: Fail to get teacher's information
      200:
        description: Get teacher's information by id
        schema:
          id: teacher_information
          properties:
            id:
              type: integer
              description: teacher's id
              default: 1
            name:
              type: string
              description: teacher's name
              default: Apple
            class:
              type: array
              description: teacher's classes
              items:
                type: string
              default: ["English", "PE", "Math"]
    """

    with open("teacher.json", "r") as json_file:
        teachers_data = json.load(json_file)

    info = {}
    for teacher_data in teachers_data:
        if teacher_data["id"] == teacher_id:
            info = teacher_data
            break

    if info == {}:
        return jsonify(info), 500
    else:
        return jsonify(info), 200


if __name__ == '__main__':
    app.run(debug=True, port=8001)
