# 기본 IMPORT
import json
import random
from typing import List
from flask_cors import CORS

from flask import Flask, request

APPLY_STUDENT_FILENAME = "apply_student.json"

data: List[List]

app = Flask(__name__)

CORS(app)


# JSON 불러오기
def load() -> List[List]:
    try:
        with open(APPLY_STUDENT_FILENAME, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return [[], []]


# JSON 저장하기
def save(apply_student: List[List]):
    with open(APPLY_STUDENT_FILENAME, 'w', encoding='utf-8') as f:
        f.write(json.dumps(apply_student))


# 신청[apply(학번, 교시)]
def apply(apply_student: List[List], student_number: int, period: int):
    # 기존에 있으면 추가 X
    for one_period in apply_student:
        for student in one_period:
            if student == student_number:
                return

    if period <= 2:
        apply_student[period - 1].append(student_number)
    else:
        raise Exception("period out of range.")


# 취소[delete(학번)]
def delete(apply_student: List[List], student_number: int):
    for one_period in apply_student:
        if student_number in one_period:
            one_period.remove(student_number)
            return


# 추첨[pop_random(인원수)]
def pop_random(apply_student: List[List], count: int):
    for one_period in apply_student:
        if len(one_period) <= count:
            continue
        else:
            while len(one_period) > count:
                one_period.pop(random.randrange(0, len(one_period) - 1))


# 신청 현황 출력하는 함수.. 필요 없다고 판단되니 주석처리 해놓음!!
# 굿
# def print_apply():
#    for n in apply_student:
#        print(n)
#    print("")

@app.route('/', methods=['GET'])
def get_info():
    global data
    return json.dumps(data)


@app.route('/apply', methods=['POST'])
def admit():
    global data  # 다 적어놓기
    data = load()

    json_data = request.get_json()

    number = int(json_data["student_number"])
    period = int(json_data["period"])
    apply(data, number, period)
    save(data)
    return "Success"


@app.route('/delete', methods=['POST'])
def cancel():
    global data
    data = load()
    json_data = request.get_json()
    number = int(json_data["student_number"])
    delete(data, number)
    save(data)
    return "Success"


def init():
    global data
    data = load()


def main():
    init()
    app.run()
    save(data)


if __name__ == '__main__':
    main()
