from flask import Flask,render_template,render_template_string,request,session, redirect, g, url_for
import mysql.connector
import logging
import sys
import cognitoConnect
from functools import wraps
from datetime import timedelta

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
app.secret_key = 'SENPOW_CLOCK_AP101'


class User:
    def __init__(self, username, fullname, email, employeeid):
        self.username = username
        self.fullname = fullname
        self.email = email
        self.employeeid = employeeid
    def __repr__(self):
        return f'<User: {self.username}>'


@app.before_request
def before_request():
    g.user = None

    if 'username' in session:
        user = User(username=session['username'], fullname=session['fullname'], email=session['email'], employeeid=session['employeeid']) 
        g.user = user

@app.before_first_request  # runs before FIRST request (only once)
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            app.logger.info("You need to login first")
            return render_template_string(""" 
            <p>Login Required.<a href="{{ url_for('login') }}"><em>Sign in</em></a> to access clock.</p>
            """)
            #return redirect(url_for('login'))
    return wrap


@app.route("/userinfo")
def home():
    clock_act = query_emp_act_db(g.user.employeeid)
    return render_template("clock_user.html",clock_act=clock_act)

@app.route("/user")
def home1():
    return "timesheet.html"



@app.route("/login", methods=['GET','POST'])
def login():
    e_nxt_msg = ''
    if request.method == 'POST':
        uname = request.form.get('username', '')
        pwd = request.form.get('password', '')
        app.logger.info(uname)
        app.logger.info(pwd)
        e_nxt_msg = valid_login(uname, pwd)
        if not e_nxt_msg:
            return redirect(url_for('clockland'))
    return render_template("ap101_login.html",e_nxt_msg=e_nxt_msg)

forgot_msg_dict = {1:"Enter UserName and Submit",2:"Enter Email code and new password",3:"New password emailed" }
@app.route("/resetpwd", methods=['GET','POST'])
def resetpwd():
    app.logger.info('in resetpwd app.py')
    app.logger.info(request.method)
    s_msg = ''
    e_msg = ''
    p_msg = ''
    #<div class="alert alert-primary">Please submmit with <strong>email verification Code</strong> and <strong>Reset password</strong> details.</div>"
    if request.method == 'GET':
        p_msg = forgot_msg_dict.get(1,'NA')
    if request.method == 'POST':
        uname = request.form.get('username', '')
        ecode  = request.form.get('ecode', '')        
        p_msg, s_msg, e_msg = forgot_pwd_nextstep(uname, ecode)

    return render_template("ap101_resetpwd.html",p_msg =p_msg , s_msg=s_msg, e_msg=e_msg)



@app.route("/signup", methods=['GET','POST'])
def signup():
    sign_dat = '' 
    uname = ''
    app.logger.info('in signup app.py')
    if request.method == 'POST':
        uname = request.form['unameser'];
        email=get_email_uname(uname)
        if request.form.get('submit_button') ==  "Create User":
            app.logger.info("Create user")
            sign_dat = signup_query(uname)
            checks, check_msg, check_debug = cognitoConnect.sign_up(uname, email, sign_dat[0][3], sign_dat[0][4], sign_dat[0][5], sign_dat[0][6], sign_dat[0][7], sign_dat[0][8])
            app.logger.info(f"Debug {check_debug}")
            app.logger.info(f"updating user {uname}")
            update_cognito_db(uname,checks,check_msg)
        if request.form.get('submit_button') == "Reset Password":
            app.logger.info("Reset Password")
            cognitoConnect.reset_pass(uname,email)
    if uname:
        app.logger.info(f"Fetching the page ap101_usercognito.html")
        sign_dat = signup_query(uname)
    return render_template("ap101_usercognito.html",sign_dat=sign_dat)

@app.route("/")
@app.route("/clockland",methods=['GET', 'POST'])
@login_required
def clockland():
    wkpct,yrpct = query_clk_stats(session['employeeid'])
    emp_def = query_emp_defaulter(session['employeeid'])
    return render_template("clock_land.html", wkpct = wkpct, yrpct = yrpct,emp_def = emp_def)


@app.route("/clock")
@login_required
def clock():
    clock_data = query_db(session['employeeid'])
    print('Quering DB', file=sys.stdout)
    return render_template("clock.html",clock_data=clock_data)


@app.route("/clocktable",  methods=['GET','POST'])
@login_required
def clocktable():
    import json
    query_dict = request.args.to_dict()
    app.logger.info(query_dict)
    app.logger.info(request.method)
    if request.method == 'GET':
        ckid = request.args.get('ckid', None)
        session['ckid'] = ckid if ckid else session['ckid']
    if request.method == 'POST':
        ckid = session['ckid']
        app.logger.info(ckid)
        information = request.data
        information = information.decode("utf-8")
        information = json.loads(information)
        app.logger.info(information)
        l_info = (information['tab_data'])
        l_action = (information['action'])
        app.logger.info(l_info)
        #chunk_size = 8
        #clock_list = [l_info[i:i+chunk_size] for i in range(0, len(l_info), chunk_size)][0]
        insert_clock(ckid,l_info,l_action)
    clock_act = get_clock_activity(g.user.employeeid)
    clock, clock_det,clock_tot  = query_clockwkdata(session['ckid'])
    app.logger.info("fetched Clockdetails for ID"+ str(session['ckid']))
    return render_template("clock_table.html",clock=clock,clock_det=clock_det,clock_act=clock_act,clock_tot=clock_tot)

@app.route("/clockfaq")
def clockfaq():
    return render_template("clock_faq.html")

@app.route("/clockthanks")
@login_required
def clockthanks():
    session.clear()
    return render_template("thanks.html")


@app.route("/clock_activity", methods = ['GET','POST'])
def clock_activity():
    if request.method == 'GET':
        return render_template("clock_activity.html")
    else:
        clock_dat = (request.form['WeekName'],request.form['EmpName'],request.form['Desc'])
        print(clock_dat)
        insert_db(clock_dat)
        return 'Here is the POST request'


def mysql_conn():
    try:
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'clk'
         }
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        logging.info("Error  in mysql"+ str(e))
        print("exception",e)


def get_email_uname(uname):
    conn,c = mysql_conn()
    logging.info("Hello in login")
    c.execute(f"""select ifnull(email,'cpathi@senthurpower.com') from emp.employee where user_name = '{uname}'""")
    user_det = c.fetchall()
    email = user_det[0][0]
    c.close()
    conn.close()
    return email


def valid_login(uname, paswd):
    conn,c = mysql_conn()
    logging.info("Hello in login")
    c.execute(f"""select user_name, concat(surname,' , ',given_name) fullname,email,employee_id from emp.employee where user_name = '{uname}'""")
    user_det = c.fetchall() 
    app.logger.info(user_det[0][3])
    c.execute(f"""SELECT clock_id from clk.clock where week_id = concat('wk',SUBSTR(YEARWEEK(SYSDATE()),3,2),'_',SUBSTR(YEARWEEK(SYSDATE()),5))and employee_id = {user_det[0][3]}""")
    wk_id = c.fetchall()
    c.execute(f"""select count(1) from emp.emp_app_roles r where role_name in ('AP101_ADMIN','AP101_USER')""")
    r_id = c.fetchall()
    c.close()
    conn.close()
    app.logger.info(user_det)   
    if len(user_det):
        response = cognitoConnect.sign_in(uname, paswd)
        app.logger.info(response)
        if str(response).find("ERR_INVALID_AUTH") != -1:
            return "Invalid Username Password."
        session['username'] = user_det[0][0]
        session['fullname'] = user_det[0][1]
        session['email'] = user_det[0][2]
        session['employeeid'] = user_det[0][3]
        session['ckid'] = wk_id[0][0]
        app.logger.info(wk_id[0][0])
        if not len(r_id):
            return "Clock not enabled for user!"
    else:
        return "Invalid Username."
    


def forgot_pwd_nextstep(uname, ecode):
    try:
        e_msg =  p_msg =  s_msg = ''
        email=get_email_uname(uname)
        if not ecode:
            response = cognitoConnect.forgot_password(uname)
            app.logger.info(response)
            if str(response).find("ERR_INVALID_FORGPASS") != -1:
                e_msg = "Invalid User details"
                p_msg = forgot_msg_dict.get(1)
            else:
                p_msg = forgot_msg_dict.get(2)
        else:
            response = cognitoConnect.confirm_forgot_password(uname, email, ecode)
            app.logger.info(response)
            if str(response).find("ERR_INVALID_CNFFORGPASS") != -1:
                e_msg = "Invalid details.Password not set"
                p_msg = forgot_msg_dict.get(2)
            else:
                s_msg = forgot_msg_dict.get(3)
    except Exception as e:
        logging.info("Error  in mysql"+ str(e))
        if not ecode:
            e_msg = "Invalid User details"
            p_msg = forgot_msg_dict.get(1)
        else:
            e_msg = "Invalid details.Password not set"
            p_msg = forgot_msg_dict.get(2)
    finally:
        logging.info(f"p_msg:{p_msg},s_msg:{s_msg},e_msg:{e_msg}")
        return p_msg, s_msg, e_msg

def signup_query(uname):
    conn,c = mysql_conn()
    logging.info("Hello in query_db")
    c.execute(f"""select uname,full_name,ema,cmg ,cognito_use,user_confirm,email_confirm
   ,(CASE
    WHEN clock_user = 1 THEN 'checked'
    ELSE null
END) clock_ad1 
   ,(CASE
    WHEN clock_admin = 1 THEN 'checked'
    ELSE null
END) clock_ad
from (select e.user_name uname,concat(e.surname,' ',e.given_name) full_name,e.email ema,(CASE
    WHEN cognito_user = 'Y' THEN 'checked'
    ELSE null
END) cognito_use,
(CASE
    WHEN user_confirmed = 'Y' THEN 'checked'
    ELSE null
END) user_confirm,
(CASE
    WHEN email_confirmed = 'Y' THEN 'checked'
    ELSE null
END) email_confirm,
(select count(1) from emp.emp_app_roles r
where e.user_name =r.user_name and role_name ='AP101_USER') clock_user,
(select count(1) from emp.emp_app_roles r
where e.user_name =r.user_name and role_name ='AP101_ADMIN') clock_admin,
cognito_msg cmg
from emp.employee e  where user_name = '{uname}') as tt""")
    clock_det = c.fetchall()
    app.logger.info(clock_det)
    c.close()
    conn.close()
    return clock_det   


def update_cognito_db(uname,checks,check_msg):
    conn,c = mysql_conn()
    logging.info("Hello in update_cognito_check_db")
    logging.info(checks)
    logging.info(check_msg)
    c.execute(f""" update emp.employee e set cognito_user ='{checks[0]}' ,user_confirmed='{checks[1]}', email_confirmed ='{checks[2]}', cognito_msg ='{check_msg}'  where user_name = '{uname}'""")
    conn.commit()
    c.close()
    conn.close()

def query_db(empid):
    conn,c = mysql_conn()
    logging.info("Hello in query_db")
    c.execute(f"""select  (@row_number:=@row_number + 1) AS a,week_id,start_date,end_date,hours_clocked,status,clock_id from clock,(SELECT @row_number:=0) AS temp where clock.employee_id = {empid} order by start_date desc""")
    clock_det = c.fetchall()
    app.logger.info(clock_det)
    c.close()
    conn.close()
    return clock_det

def query_clk_stats(empid):
    conn,c = mysql_conn()
    logging.info("Hello in query_clock stats")
    c.execute(f"""SELECT clock_id from clk.clock where week_id = concat('wk',SUBSTR(YEARWEEK(SYSDATE()),3,2),'_',SUBSTR(YEARWEEK(SYSDATE()),5))and employee_id = {empid}""")
    wk_id = c.fetchall()
    ckid = wk_id[0][0]
    c.execute(f"""select round((IFNULL((hours_clocked),0)/45) *100,2) from clock where clock_id = {ckid} and employee_id = {empid}""")
    wkpct = c.fetchall()
    app.logger.info(wkpct)
    c.execute(f"""select round(((tot/(cnt*45))*100),2) from(select sum(IFNULL((hours_clocked),0)) tot,count(1) AS cnt from clock where ((YEAR(CURRENT_DATE()) = YEAR(start_date)) OR (YEAR(CURRENT_DATE()) = YEAR(end_date))) and employee_id = {empid}) a""")
    yrpct = c.fetchall()
    app.logger.info(yrpct)
    c.close()
    conn.close()
    return wkpct[0][0],yrpct[0][0]

def query_emp_act_db(empid):
    conn,c = mysql_conn()
    logging.info("Hello in employee activity db")
    c.execute(f"""select p.project_name,t.description,a.activity_code,a.activity_desc,a.start_date,a.end_date  from clock_activity a, prj.projects p,prj.project_task t where employee_id ={empid} and t.task_id = a.task_id and t.project_id = p.project_id""")
    clock_act = c.fetchall()
    app.logger.info(clock_act)
    c.close()
    conn.close()
    return clock_act

def query_emp_defaulter(empid):
    conn,c = mysql_conn()
    logging.info("Hello in employee defaulters")
    c.execute(f""" select concat(e.surname,e.given_name) full_name,week_id,hours_clocked,status from clk.clock c,emp.employee e,emp.employee m where e.employee_id = c.employee_id and e.manager_id = m.employee_id and m.employee_id ={empid} and c.status != 'Submitted'  order by 1,2""")
    clock_act = c.fetchall()
    app.logger.info(clock_act)
    c.close()
    conn.close()
    return clock_act

def query_clockwkdata(ckid):
    logging.info("Hello in query_db")
    conn,c = mysql_conn()
    c.execute(f"""select clock_id,start_date,start_date_plus1,start_date_plus2 ,start_date_plus3 ,start_date_plus4 ,start_date_plus5,end_date,week_id from clock where clock_id ={ckid} """)
    clock = c.fetchall()
    app.logger.info('Fetched Details')
    c.execute(f"""select c.activity_id , c.day1,c.day2,c.day3,c.day4,c.day5,c.day6,c.day7,c.seq_no,a.activity_code from clock_details c,clock_activity a where clock_id = {ckid} and c.activity_id = a.activity_id order by seq_no """)
    clock_det = c.fetchall()
    app.logger.info('Fetched Activity details')
    c.execute(f"""select IFNULL(day1,0),IFNULL(day2,0),IFNULL(day3,0),IFNULL(day4,0),IFNULL(day5,0),IFNULL(day6,0),IFNULL(day7,0),CONCAT('Week Tot:',IFNULL((day1+day2+day3+day4+day5+day6+day7),0)) tot from (select  sum(IFNULL(c.day1,0)) day1,sum(IFNULL(c.day2,0)) day2,sum(IFNULL(c.day3,0)) day3,sum(IFNULL(c.day4,0)) day4,sum(IFNULL(c.day5,0)) day5,sum(IFNULL(c.day6,0)) day6,sum(IFNULL(c.day7,0)) day7 from clock_details c where clock_id = {ckid})d """)
    clock_tot = c.fetchall()
    app.logger.info('Fetched Activity details')
    c.close()
    conn.close()
    return clock, clock_det, clock_tot


def get_clock_activity(empid):
    conn,c = mysql_conn()
    c.execute(f"""select  activity_code,activity_id from clock_activity where employee_id ={empid}""")
    clock_act = c.fetchall()
    c.close()
    conn.close()
    return clock_act


def insert_db(clock_act):
    logging.info("Hello in query_db")
    conn,c = mysql_conn()
    sql_qry = " INSERT INTO clock_details (week_name , emp_name, description) values (?,?,?)"
    c.execute(sql_qry,clock_act)
    clock_det = c.fetchall()
    c.close()
    conn.close()
    return clock_det

def insert_clock(ckid,clock_data,action):
    try:
        conn,c = mysql_conn()
        clock_act = get_clock_activity(g.user.employeeid)
        clock_act = dict(clock_act)
        app.logger.info(clock_data)
        tot_hrs = 0   
        sqlquery = f""" Delete  from  clock_details where clock_id = {ckid}"""
        app.logger.info(sqlquery)
        c.execute(sqlquery) 
        for cnt,clock_dat in enumerate(clock_data):
            if cnt == len(clock_data)-1:
                continue
            clock_dat[0] = clock_act.get(clock_dat[0])
            clock_dat.insert(0,ckid)
            sqlquery = f""" Insert into clock_details (clock_id ,activity_id , day1,day2,day3,day4,day5, day6,day7) values 
                       {tuple(clock_dat)}"""
            app.logger.info(sqlquery)
            c.execute(sqlquery)
            tot_hrs += sum([int(i) for i in list(tuple(clock_dat))][2:])
        sqlquery = f""" Update clock set hours_clocked = {tot_hrs},submitted_date = date(sysdate()),status = '{action}',update_ts = CURRENT_TIMESTAMP() where clock_id = {ckid}"""
        app.logger.info(sqlquery)
        c.execute(sqlquery)
        c.close()
        conn.commit()
        conn.close()
    except Exception as e:
        app.logger.info(e)




if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
