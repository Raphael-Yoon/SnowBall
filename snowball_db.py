import sqlite3

def get_user_list():
    print('get_user_list function')
    con = sqlite3.connect("snowball.db")
    cur = con.cursor()
    sql = "select company_name from sb_user order by user_name"
    cur.execute(sql)
    result = cur.fetchall()
    con.close()
    modified_result = [item for sublist in result for item in sublist]
    return modified_result

def get_login(company_name, login_key):
    print('get_login function')
    con = sqlite3.connect("snowball.db")
    cur = con.cursor()
    sql = "select company_name from sb_user where company_name='{}' and login_key='{}'".format(company_name, login_key)
    print('login = ', sql)
    cur.execute(sql)
    result = cur.fetchone()
    con.close()
    return result

def set_login(company_name, login_key):
    print('set_login function')
    con = sqlite3.connect("snowball.db")
    cur = con.cursor()
    sql = "insert into sb_user_log(user_id, log_date, log_type) select user_id, datetime('now', 'localtime'), 'Log in' as log_type from sb_user where company_name='{}' and login_key='{}'".format(company_name, login_key)
    result = cur.execute(sql)
    print('result = ', result)
    con.commit()
    con.close()
    return result

def get_user_request():
    con = sqlite3.connect("snowball.db")
    cur = con.cursor()
    sql = "select company_name, user_name, user_email, interface_yn, creation_date, request_id from sb_user_request"
    print('sql = ', sql)
    cur.execute(sql)
    result = cur.fetchall()
    print('result = ', result)
    con.close()
    return result

def set_user_regist_request(company_name, user_name, user_email):
    con = sqlite3.connect("snowball.db")
    cur = con.cursor()
    sql = "insert into sb_user_request(company_name, user_name, user_email, interface_yn, creation_date) values('{}', '{}', '{}', 'N', datetime('now', 'localtime'))".format(company_name, user_name, user_email)
    print('sql = ', sql)
    result = cur.execute(sql)
    print('result = ', result)
    con.commit()
    con.close()
    return result

def set_rcm_request(pi_request_type, pi_request_file, pi_client_name, pi_email_address):
    con = sqlite3.connect("snowball.db")
    cur = con.cursor()
    sql = "insert into sb_request(request_id, request_type, request_file, client_name, email_address, request_date) values(1, {}, {}, {}, {}, datetime('now', 'localtime'))".format(pi_request_type, pi_request_file, pi_client_name, pi_email_address)
    print('sql = ', sql)
    result = cur.execute(sql)
    print('result = ', result)
    con.commit()
    con.close()
    return result

def set_paper_request(pi_client_name, pi_email, pi_request_file, pi_request_content):
    print('set_paper_request')
    con = sqlite3.connect("snowball.db")
    cur = con.cursor()
    sql = "insert into sb_request(request_id, request_file, client_name, email_address, request_date, request_content) values(1, '{}', '{}', '{}', datetime('now', 'localtime'))".format(pi_request_file, pi_client_name, pi_email, pi_request_content)
    print('sql = ', sql)
    result = cur.execute(sql)
    print('result = ', result)
    con.commit()
    con.close()
    return result
