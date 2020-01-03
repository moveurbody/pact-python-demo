# -*- coding: utf-8 -*-
# @Time    : 2019/12/24 下午3:43
# @Author  : yu_hsuan_chen@trendmicro.com
# @File    : student
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
@app.route('/api/students/init', methods=['POST'])
def init():
    data = [
        {
            "id": 1,
            "name": "Eric",
            "class": [
                "Chinese"
            ],
            "age": 10
        },
        {
            "id": 2,
            "name": "Jason",
            "class": [
                "Chinese",
                "Chemistry"
            ],
            "age": 11
        }
    ]

    with open("teacher.json", "w") as json_file:
        json.dump(data, json_file)

    return jsonify({"states": "OK"})


@app.route('/api/students/', methods=['GET'])
def students():
    """
    Use the API to get all students information
    ---
    tags:
      - Get all students information
    responses:
      500:
        description: Fail to get all students information
      200:
        description: Get all students information
        schema:
          type: array
          items:
            $ref: "#/definitions/student_information"
    """
    with open("student.json", "r") as json_file:
        students_data = json.load(json_file)

    return jsonify(students_data), 200


@app.route('/api/students/<int:student_id>', methods=['GET'])
def student(student_id):
    """
    Use the API to get student information by id
    ---
    tags:
      - Get all students information
    produces:
      - application/json
    parameters:
      - name: student_id
        in: path
        type: integer
        required: true
        description: student id
        x-example: 1
    responses:
      200:
        description: Get student's information by id
        schema:
          id: student_information
          properties:
            id:
              type: integer
              description: student's id
              default: 1
            name:
              type: string
              description: student's name
              default: Eric
            age:
              type: integer
              description: student's age
              default: 10
            class:
              type: array
              description: student's classes
              items:
                type: string
              default: ["Chinese"]
          required:
            - id
            - name
            - class
            - age
    """

    with open("student.json", "r") as json_file:
        student_data = json.load(json_file)

    info = {}
    for student_data in student_data:
        if student_data["id"] == student_id:
            info = student_data
            break

    if info == {}:
        return jsonify(info), 500
    else:
        return jsonify(info), 200


if __name__ == '__main__':
    app.run(debug=True, port=8002)
