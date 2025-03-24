from flask import Flask, render_template, request, send_file, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, current_user
from openpyxl import load_workbook
import pandas as pd
import os
from datetime import datetime

import link_admin
import link1_rcm
import link1_pbc
import link2_design
import link3_operation
import snowball_db

app = Flask(__name__)
app.secret_key = '150606'

@app.route('/')
def index():
    result = snowball_db.get_user_list()
    return render_template('index.jsp', user_name = result, return_code=0)

def main():
    app.run(host='0.0.0.0', debug=False, port=5001)
    #app.run(host='127.0.0.1', debug=False, port=8001)

@app.route('/link_admin')
def link():
    print("Admin Function")
    result = snowball_db.get_user_request()
    return render_template('link0.jsp', login_code = 0)

@app.route('/link0')
def link0():
    print("Reload")
    return render_template('link0.jsp')

@app.route('/link1')
def link1():
    print("RCM Function")
    return render_template('link1.jsp', return_code=0)

s_questions = [
    {"index": 0, "text": "시스템 이름을 적어주세요."},
    {"index": 1, "text": "사용하고 있는 시스템은 상용소프트웨어입니까?"},
    {"index": 2, "text": "기능을 회사내부에서 수정하여 사용할 수 있습니까?(SAP, Oracle ERP 등등)"},
    {"index": 3, "text": "Cloud 서비스를 사용하고 있습니까?"},
    {"index": 4, "text": "어떤 종류의 Cloud입니까?"},
    {"index": 5, "text": "Cloud 서비스 업체에서는 SOC1 Report를 발행하고 있습니까?"},
    {"index": 6, "text": "OS 접근제어 Tool을 사용하고 있습니까?"},
    {"index": 7, "text": "DB 접근제어 Tool을 사용하고 있습니까?"},
    {"index": 8, "text": "별도의 Batch Schedule Tool을 사용하고 있습니까?"},
    {"index": 9, "text": "사용자 권한부여 이력이 시스템에 기록되고 있습니까?"},
    {"index": 10, "text": "사용자 권한회수 이력이 시스템에 기록되고 있습니까?"},
    {"index": 11, "text": "사용자가 새로운 권한이 필요한 경우 요청서를 작성하고 부서장 등의 승인을 득하는 절차가 있습니까?"},
    {"index": 12, "text": "권한이 부여되는 절차를 기술해 주세요."},
    {"index": 13, "text": "부서이동 등 기존권한의 회수가 필요한 경우 수행되는 절차를 기술해 주세요."},
    {"index": 14, "text": "퇴사자 발생시 접근권한을 차단하는(계정 삭제 등) 절차를 기술해 주세요."},
    {"index": 15, "text": "전체 사용자가 보유한 권한에 대한 적절성을 모니터링하는 절차가 있습니까?"},
    {"index": 16, "text": "패스워드 설정사항을 기술해 주세요."},
    {"index": 17, "text": "데이터 변경 이력이 시스템에 기록되고 있습니까?(쿼리로 변경)."},
    {"index": 18, "text": "데이터 변경이 필요한 경우 요청서를 작성하고 부서장 등의 승인을 득하는 절차가 있습니까?"},
    {"index": 19, "text": "DB 접근권한 부여 이력이 시스템에 기록되고 있습니까?"},
    {"index": 20, "text": "DB 접근권한이 필요한 경우 요청서를 작성하고 부서장 등의 승인을 득하는 절차가 있습니까?"},
    {"index": 21, "text": "DB 관리자 권한을 보유한 인원에 대해 기술해 주세요."},
    {"index": 22, "text": "DB 패스워드 설정사항을 기술해 주세요."},
    {"index": 23, "text": "OS 접근권한 부여 이력이 시스템에 기록되고 있습니까?"},
    {"index": 24, "text": "OS 접근권한이 필요한 경우 요청서를 작성하고 부서장 등의 승인을 득하는 절차가 있습니까?"},
    {"index": 25, "text": "OS 관리자 권한을 보유한 인원에 대해 기술해 주세요."},
    {"index": 26, "text": "OS 패스워드 설정사항을 기술해 주세요."},
    {"index": 27, "text": "프로그램 변경 이력이 시스템에 기록되고 있습니까?"},
    {"index": 28, "text": "프로그램 변경이 필요한 경우 요청서를 작성하고 부서장의 승인을 득하는 절차가 있습니까?"},
    {"index": 29, "text": "프로그램 변경시 사용자 테스트를 수행하고 그 결과를 문서화하는 절차가 있습니까?"},
    {"index": 30, "text": "프로그램 변경 완료 후 이관(배포)을 위해 부서장 등의 승인을 득하는 절차가 있습니까?"},
    {"index": 31, "text": "이관(배포)권한을 보유한 인원에 대해 기술해 주세요."},
    {"index": 32, "text": "운영서버 외 별도의 개발 또는 테스트 서버를 운용하고 있습니까?"},
    {"index": 33, "text": "배치 스케줄 등록/변경 이력이 시스템에 기록되고 있습니까?"},
    {"index": 34, "text": "배치 스케줄 등록/변경이 필요한 경우 요청서를 작성하고 부서장 등의 승인을 득하는 절차가 있습니까?"},
    {"index": 35, "text": "배치 스케줄을 등록/변경할 수 있는 인원에 대해 기술해 주세요."},
    {"index": 36, "text": "배치 실행 오류 등에 대한 모니터링은 어떻게 수행되고 있는지 기술해 주세요."},
    {"index": 37, "text": "백업은 어떻게 수행되고 또 어떻게 모니터링되고 있는지 기술해 주세요."},
    {"index": 38, "text": "장애 발생시 이에 대응하고 조치하는 절차에 대해 기술해 주세요."},
    {"index": 39, "text": "서버실 출입시의 절차에 대해 기술해 주세요."}
]

question_count = len(s_questions)

@app.route('/link2', methods=['GET', 'POST'])
def link2():
    print("Question Function")

    if request.method == 'GET':
        # 세션 초기화
        session.clear()
        session['question_index'] = 0
        session['answer'] = [''] * question_count  # 필요한 만큼 동적으로 조절 가능
        session['System'] = ''
        session['Cloud'] = ''
        session['OS_Tool'] = ''
        session['DB_Tool'] = ''
        session['Batch_Tool'] = ''

    question_index = session['question_index']

    if request.method == 'POST':
        form_data = request.form
        session['answer'][question_index] = form_data.get(f"a{question_index}", '')
        if form_data.get('a1_1'):
            session['System'] = form_data.get('a1_1')
        if form_data.get('a4_1'):
            session['Cloud'] = form_data.get('a4_1')
        if form_data.get('a6_1'):
            session['OS_Tool'] = form_data.get('a6_1')
        if form_data.get('a7_1'):
            session['DB_Tool'] = form_data.get('a7_1')
        if form_data.get('a8_1'):
            session['Batch_Tool'] = form_data.get('a8_1')

        # 다음 질문 인덱스를 결정하는 매핑

        next_question = {
            0: 1,
            1: 2 if session['answer'][question_index] == 'Y' else 3,
            2: 3,  # 동일한 흐름을 가지므로 조건 필요 없음
            3: 4 if session['answer'][question_index] == 'Y' else 6,
            4: 5,
            5: 6,
            6: 7,
            7: 8,
            8: 9,
            9: 10,
            10: 11,
            11: 12,
            12: 13,
            13: 14,
            14: 15,
            15: 16,
            16: 17,
            17: 18,
            18: 19,
            19: 20,
            20: 21,
            21: 22,
            22: 23,
            23: 24,
            24: 25,
            25: 26,
            26: 27,
            27: 28,
            28: 29,
            29: 30,
            30: 31,
            31: 32,
            32: 33,
            33: 34,
            34: 35,
            35: 36,
            36: 37,
            37: 38,
            38: 39,
            39: 40,
        }

        session['question_index'] = next_question.get(question_index, question_index)
        print(f"goto {session['question_index']}")

        # 현재 응답 상태 출력 (join 사용)
        print("Answers:", ", ".join(f"{i}: {ans}" for i, ans in enumerate(session['answer'])))
        
        if session['question_index'] > 4: #question_count:
            print('excel download')
            return save_to_excel()

    # 현재 질문을 렌더링
    question = s_questions[session['question_index']]
    return render_template('link2_system.jsp', question=question['text'], question_number=session['question_index'])
    
@app.route('/export_excel', methods=['GET'])
def save_to_excel():
    answers = session.get('answer', [])
    system_info = [session.get(key, '') for key in ['System', 'Cloud', 'OS_Tool', 'DB_Tool', 'Batch_Tool']]
    today = datetime.today().strftime('%Y%m%d')
    file_name = f"{answers[0]}_{today}.xlsx" if answers else f"responses_{today}.xlsx"
    
    df = pd.DataFrame({'Question': [q['text'] for q in s_questions], 'Answer': answers}).fillna('')
    df.loc[[1, 3, 6, 7, 8], 'Extra Info'] = system_info
    file_path = os.path.join("static", file_name)
    
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Responses', index=False)
        worksheet = writer.sheets['Responses']
        worksheet.set_column('A:A', max(df['Question'].apply(len)) + 2)
    
    return send_file(file_path, as_attachment=True)


'''
@app.route('/link2', methods=['GET', 'POST'])
def link2():
    print("Question Function")

    if request.method == 'GET':
        # 세션을 열 때마다 초기화
        session.clear()  # 모든 세션 값 초기화
        session['question_index'] = 0
        session['answer'] = ['']*9

    question_index = session['question_index']
    question = s_questions[question_index]

    # POST 요청 처리 (다음 버튼을 눌렀을 때)
    
    if request.method == 'POST':
        form_data = request.form
        if session['question_index'] == 0: #0: 사용하고 있는 시스템은 상용소프트웨어(Package S/W)입니까?
            session['answer'][question_index] = form_data.get("a0")
            print(f"1 = {session['answer'][question_index]}")
            if session['answer'][question_index] == 'Y':
                session['question_index'] = 1
                print('goto 1')
            elif session['answer'][question_index] == 'N':
                session['question_index'] = 2
                print('goto 2')

        elif session['question_index'] == 1: #1: 기능을 회사내부에서 수정하여 사용할 수 있습니까?(SAP, Oracle ERP 등등)
            session['answer'][question_index] = form_data.get("a1")
            print(f"1 = {session['answer'][question_index]}")
            if session['answer'][question_index] == 'Y':
                session['question_index'] = 2
                print('goto 2')
            elif session['answer'][question_index] == 'N':
                session['question_index'] = 2
                print('goto 3')

        elif session['question_index'] == 2: #2	Cloud 서비스를 사용하고 있습니까?
            session['answer'][question_index] = form_data.get("a2")
            if session['answer'][question_index] == 'Y':
                session['question_index'] = 3
                print('goto 3')
            elif session['answer'][question_index] == 'N':
                session['question_index'] = 5
                print('goto 5')

        elif session['question_index'] == 3: #3	어떤 종류의 Cloud입니까?
            session['answer'][question_index] = form_data.get("a3")
            session['question_index'] = 4
            print('goto 4')

        elif session['question_index'] == 4: #4	Cloud 서비스 업체에서는 SOC1 Report를 발행하고 있습니까?
            session['answer'][question_index] = form_data.get("a4")
            session['question_index'] = 5
            print('goto 5')

        elif session['question_index'] == 5: #5	OS 접근제어 Tool 사용 여부
            session['answer'][question_index] = form_data.get("a5")
            session['question_index'] = 6
            print('goto 6')

        elif session['question_index'] == 6: #6	DB 접근제어 Tool 사용 여부
            session['answer'][question_index] = form_data.get("a6")
            session['question_index'] = 7
            print('goto 7')

        elif session['question_index'] == 7: #7	Batch Schedule Tool 사용 여부
            session['answer'][question_index] = form_data.get("a7")
            session['question_index'] = 8
            print('goto 8')

        print(f"0: {session['answer'][0]}, 1: {session['answer'][1]}, 2: {session['answer'][2]}, 3: {session['answer'][3]}, 4: {session['answer'][4]}, 5: {session['answer'][5]}, 6: {session['answer'][6]}, 7: {session['answer'][7]}")
        print('index = ', session['question_index'])

    # 현재 질문을 렌더링
    question = s_questions[session['question_index']]

    return render_template('link2_system.jsp', question=question['text'], question_number=session['question_index']+1)
'''

@app.route('/link3')
def link3():
    print("Paper Function")
    return render_template('link3.jsp')

@app.route('/link4')
def link4():
    print("Education Function")
    return render_template('link4.jsp')

@app.route('/link9')
def link9():
    print("ETC Function")
    return render_template('link9.jsp')

@app.route('/login', methods=['POST'])
def login():
    print('login function')
    form_data = request.form.to_dict()

    param1 = form_data.get('param1')
    param2 = form_data.get('param2')

    print("Param1 = ", param1)
    print("Param2 = ", param2)

    result = snowball_db.get_login(param1, param2)

    if result:
        print("Login Success")
        snowball_db.set_login(param1, param2)
        return render_template('link0.jsp', login_id = param1, login_code = 0)
    else:
        print("Login Fail")
        result = snowball_db.get_user_list()
        return render_template('index.jsp', user_name = result, return_code=1)

@app.route('/register', methods=['POST'])
def register():
    print("Register")
    return render_template('register.jsp')

@app.route('/register_request', methods=['POST'])
def register_request():
    print("Register request")

    form_data = request.form.to_dict()

    param1 = form_data.get('param1')
    param2 = form_data.get('param2')
    param3 = form_data.get('param3')

    print("Param1 = ", param1)
    print("Param2 = ", param2)
    print("Param3 = ", param3)

    result = snowball_db.set_user_regist_request(param1, param2, param3)
    result = snowball_db.get_user_list()
    return render_template('index.jsp', user_name = result, return_code=2)

@app.route('/set_regist', methods=['POST'])
def set_regist():

    form_data = request.form.to_dict()

    result = link_admin.set_regist(form_data)

    request_list = snowball_db.get_user_request()
    return render_template('link.jsp', user_request = request_list)
    
@app.route('/rcm_generate', methods=['POST'])
def rcm_generate():

    form_data = request.form.to_dict()
    output_path = link1_rcm.rcm_generate(form_data)

    return send_file(output_path, as_attachment=True)

@app.route('/rcm_request', methods=['POST'])
def rcm_request():

    form_data = request.form.to_dict()
    link1_rcm.rcm_request(form_data)

    return render_template('link1.jsp', return_code=1)

@app.route('/paper_request', methods=['POST'])
def paper_request():
    print("Paper Request called")

    form_data = request.form.to_dict()
    output_path = link2_design.paper_request(form_data)

    return render_template('link2.jsp', return_code = 2)

@app.route('/design_generate', methods=['POST'])
def design_generate():
    print("Design Generate called")

    form_data = request.form.to_dict()
    output_path = link2_design.design_generate(form_data)

    return send_file(output_path, as_attachment=True)

@app.route('/design_template_download', methods=['POST']) 
def design_template_downloade():
    print("Design Template Download called")

    form_data = request.form.to_dict()
    output_path = link2_design.design_template_download(form_data)

    return send_file(output_path, as_attachment=True)

@app.route('/paper_template_download', methods=['POST'])
def paper_template_download():

    form_data = request.form.to_dict()
    output_path = link3_operation.paper_template_download(form_data)

    param1 = form_data.get('param1')
    param2 = form_data.get('param2')

    print('output = ', output_path)
    if output_path != '':
        return send_file(output_path, as_attachment=True)
    else:
        return render_template('link3.jsp', return_param1=param1, return_param2=param2)

@app.route('/paper_generate', methods=['POST'])
def paper_generate():

    form_data = request.form.to_dict()
    output_path = link3_operation.paper_generate(form_data)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    main()