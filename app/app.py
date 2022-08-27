from flask import Flask,render_template,render_template_string,request,session, redirect, g, url_for
import mysql.connector
import logging
import sys
import cognitoConnect
from functools import wraps

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
app.secret_key = 'SENPOW_CLOCK_AP101'


class User:
    def __init__(self, username, fullname, email):
        self.username = username
        self.fullname = fullname
        self.email = email
    def __repr__(self):
        return f'<User: {self.username}>'


@app.before_request
def before_request():
    g.user = None

    if 'username' in session:
        user = User(username=session['username'], fullname=session['fullname'], email=session['email']) 
        g.user = user


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
        p_msg, s_msg, e_msg = forgot_pwd_nextstep()

    return render_template("ap101_resetpwd.html",p_msg =p_msg , s_msg=s_msg, e_msg=e_msg)



@app.route("/signup", methods=['GET','POST'])
def signup():
    sign_dat = '' 
    uname = ''
    app.logger.info('in signup app.py')
    if request.method == 'POST':
        uname = request.form['unameser'];
        if request.form.get('submit_button') ==  "Create User":
            app.logger.info("Create user")
            sign_dat = signup_query(uname)
            checks, check_msg, check_debug = cognitoConnect.sign_up(uname, sign_dat[0][3], sign_dat[0][4], sign_dat[0][5], sign_dat[0][6], sign_dat[0][7], sign_dat[0][8])
            app.logger.info(f"Debug {check_debug}")
            app.logger.info(f"updating user {uname}")
            update_cognito_db(uname,checks,check_msg)
        if request.form.get('submit_button') == "Reset Password":
            app.logger.info("Reset Password")
            cognitoConnect.reset_pass(uname)
    if uname:
        app.logger.info(f"Fetching the page ap101_usercognito.html")
        sign_dat = signup_query(uname)
    return render_template("ap101_usercognito.html",sign_dat=sign_dat)

@app.route("/")
@app.route("/clockland",methods=['GET', 'POST'])
@login_required
def clockland():
    return render_template("clock_land.html")


@app.route("/clock")
@login_required
def clock():
    clock_data = query_db()
    print('Quering DB', file=sys.stdout)
    return render_template("clock.html",clock_data=clock_data)


@app.route("/clocktable",  methods=['GET','POST'])
@login_required
def clocktable():
    query_dict = request.args.to_dict()
    app.logger.info(query_dict)
    if request.method == 'GET':
        ckid = request.args.get('ckid', None)
        session['ckid'] = ckid
        clock, clock_det,clock_act,clock_tot  = query_clockwkdata(ckid)
        app.logger.info("fetched Clockdetails for ID"+ str(ckid))
        return render_template("clock_table.html",clock=clock,clock_det=clock_det,clock_act=clock_act,clock_tot=clock_tot)
    if request.method == 'POST':
        ckid = session['ckid']
        app.logger.info(ckid)
        information = request.data
        app.logger.info(request.method)
        app.logger.info(type(information))
        l_info = (information.decode("utf-8")).split(',')
        chunk_size = 8
        clock_list = [l_info[i:i+chunk_size] for i in range(0, len(l_info), chunk_size)]
        app.logger.info(clock_list)
        insert_clock(ckid,clock_list)

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


def valid_login(uname, paswd):
    conn,c = mysql_conn()
    logging.info("Hello in login")
    c.execute(f"""select user_name, concat(surname,' , ',given_name) fullname,email,employee_id from emp.employee where user_name = '{uname}'""")
    user_det = c.fetchall() 
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
    else:
        return "Invalid Username."


def forgot_pwd_nextstep(username, ecode):
    if not ecode:
        response = cognitoConnect.forgot_password(uname)
        if str(response).find("ERR_INVALID_FORGPASS") != -1:
            e_msg = "Invalid User details"
            p_msg = forgot_msg_dict.get(1)
        else:
            p_msg = forgot_msg_dict.get(2)
    else:
        response = cognitoConnect.confrim_forgot_password(uname, ecode)
        if str(response).find("ERR_INVALID_CNFFORGPASS") != -1:
            e_msg = "Invalid details.Password not set"
            p_msg = forgot_msg_dict.get(2)
        else:
            s_msg = forgot_msg_dict.get(3)
    return "Enter Vaild Username and submmit"


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

def query_db():
    conn,c = mysql_conn()
    logging.info("Hello in query_db")
    c.execute(f"""select  (@row_number:=@row_number + 1) AS a,week_id,start_date,end_date,hours_clocked,status,clock_id from clock,(SELECT @row_number:=0) AS temp order by start_date desc""")
    clock_det = c.fetchall()
    app.logger.info(clock_det)
    c.close()
    conn.close()
    return clock_det



def query_emp_act_db(empid):
    conn,c = mysql_conn()
    logging.info("Hello in employee activity db")
    c.execute(f"""select p.project_name,t.description,a.activity_code,a.start_date,a.end_date  from clock_activity a, prj.projects p,prj.project_task t where employee_id ={empid} and t.task_id = a.task_id and t.project_id = p.project_id""")
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
    clock_act = get_clock_activity()
    app.logger.info('Fetched Activity details')
    c.execute(f"""select IFNULL(day1,0),IFNULL(day2,0),IFNULL(day3,0),IFNULL(day4,0),IFNULL(day5,0),IFNULL(day6,0),IFNULL(day7,0),CONCAT('Week Tot:',IFNULL((day1+day2+day3+day4+day5+day6+day7),0)) tot from (select  sum(IFNULL(c.day1,0)) day1,sum(IFNULL(c.day2,0)) day2,sum(IFNULL(c.day3,0)) day3,sum(IFNULL(c.day4,0)) day4,sum(IFNULL(c.day5,0)) day5,sum(IFNULL(c.day6,0)) day6,sum(IFNULL(c.day7,0)) day7 from clock_details c where clock_id = {ckid})d """)
    clock_tot = c.fetchall()
    app.logger.info('Fetched Activity details')
    c.close()
    conn.close()
    return clock, clock_det, clock_act, clock_tot


def get_clock_activity():
    conn,c = mysql_conn()
    c.execute(f"""select  activity_code,activity_id from clock_activity """)
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

def insert_clock(ckid,clock_data):
    try:
        conn,c = mysql_conn()
        clock_act = get_clock_activity()
        clock_act = dict(clock_act)
        app.logger.info(clock_act)
        app.logger.info(request.query_string)
        app.logger.info('Hello')    
        for cnt,clock_dat in enumerate(clock_data):
            if cnt == len(clock_data)-1:
                continue
            
            app.logger.info(clock_act.get(clock_dat[0]))
            clock_dat[0] = clock_act.get(clock_dat[0])
            clock_dat.insert(0,ckid)
            app.logger.info(clock_dat)
            sqlquery = f""" Delete  from  clock_details where clock_id = {ckid}"""
            app.logger.info(sqlquery)
            c.execute(sqlquery)
            sqlquery = f""" Insert into clock_details (clock_id ,activity_id , day1,day2,day3,day4,day5, day6,day7) values 
                       {tuple(clock_dat)}"""
            app.logger.info(sqlquery)
            c.execute(sqlquery)
        c.close()
        conn.commit()
        conn.close()
    except Exception as e:
        app.logger.info(e)




if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
