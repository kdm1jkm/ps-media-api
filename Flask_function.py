#기본 IMPORT
from flask import Flask, request
import json
import random

app=Flask(__name__)

#기본 리스트
apply_student_1 = []
apply_student_2 = []
apply_student = [apply_student_1, apply_student_2]

#JSON 불러오기
def load():
    with open('apply_student.json', 'r', encoding='utf-8') as apply_rate:
        temp = apply_rate.read()
        apply_student = json.loads(temp)
        return apply_student
   
#JSON 저장하기
def save():
    with open('apply_student.json', 'w', encoding='utf-8') as apply_rate:
        apply_rate.write(json.dumps(apply_student))

#신청[apply(학번, 교시)]
def apply(student_number, period):
    #기존에 있으면 추가 X
    for find in apply_student:
        for search in find:
            if search == student_number:
                return
            
    if period <= 2:
        apply_student[period - 1].append(student_number)


#취소[delete(학번)]
def delete(student_number):
    for find in apply_student:
        i = 0
        for search in find:
            if search == student_number:
                find.pop(i)
            i += 1

#추첨[pop_random(인원수)]
def pop_random(count):
    
    for find in apply_student:
        if len(find) <= count:
            continue
        else:
            while len(find) > count:
                find.pop(random.randrange(0, len(find) - 1))

#신청 현황 출력하는 함수.. 필요 없다고 판단되니 주석처리 해놓음!!
# def print_apply():
#    for n in apply_student:
#        print(n)
#    print("")

@app.route('/', methods=['GET'])
def get_info():
    global apply_student
    return json.dumps(apply_student)

@app.route('/apply', methods=['POST'])
def admit():
    global apply_student #다 적어놓기
    apply_student = load()
    number = int(request.headers.get("student_number"))
    period = int(request.headers.get("period"))
    apply(number, period)
    save()

@app.route('/delete', methods=['POST'])
def disadmit():
    global apply_student
    apply_student = load()
    number = int(request.headers.get("student_number"))
    delete(number)
    save()

if __name__ == '__main__':
    apply_student = load()
    app.run()
    save()