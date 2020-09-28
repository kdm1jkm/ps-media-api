import json


# JSON 불러오기
def load():
    with open('all_student.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())


# JSON 저장하기
def save(old_student):
    with open('all_student.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(old_student, ensure_ascii=False))


def main():
    school_num = input("학번을 입력하세요 : ")
    name = input("이름을 입력하세요 : ")
    lib_num = input("도서관 몇 실 인가요? : ")
    seat_num = input("자리 몇 번 이나요? : ")

    if int(seat_num) < 10:
        num_seat = int(lib_num + str(0) + str(0) + seat_num)
        new_student = {school_num: {"name": name, "seat_num": str(num_seat), "school_num": school_num}}
    else:
        num_seat = int(lib_num + str(0) + seat_num)
        new_student = {school_num: {"name": name, "seat_num": str(num_seat), "school_num": school_num}}
    old_student = load()
    old_student.update(new_student)
    save(old_student)


if __name__ == '__main__':
    main()
