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
app.config['SWAGGER'] = {
    'title': 'Teachers API Documents',
    "specs": [
            {
                "endpoint": 'swagger',
                "route": '/swagger.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
}

Swagger(app)


# Generate data as database
@app.route('/api/teachers/init', methods=['POST'])
def init():
    data = [
        {
            "id": 1,
            "name": "Doris Wilson",
            "class": [
                "Chinese",
                "English"
            ]
        },
        {
            "id": 2,
            "name": "Mrs. A. T. Whitecotton",
            "class": [
                "Physics",
                "Chemistry"
            ]
        }
    ]

    with open("teacher.json", "w") as json_file:
        json.dump(data, json_file)

    return jsonify({"states": "OK"})


@app.route('/api/teachers/', methods=['GET'])
def teachers():
    """
    Use the API to get all teachers information
    ---
    tags:
      - Get all teachers information
    produces:
    - application/json
    responses:
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
    produces:
    - application/json
    parameters:
      - name: teacher_id
        in: path
        required: true
        type: integer
        description: teacher id
        x-example: 1
    responses:
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
        return jsonify(info), 400
    else:
        return jsonify(info), 200


if __name__ == '__main__':
    app.run(debug=True, port=8001)
