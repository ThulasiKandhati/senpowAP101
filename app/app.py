from flask import Flask,render_template,request,session
import mysql.connector
import logging
import sys

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
app.secret_key = 'SENPOW_CLOCK_AP101'

@app.route("/userinfo")
def home():
    clock_user = query_emp_db(1000)
    clock_act = query_emp_act_db(1000)
    return render_template("clock_user.html",clock_user=clock_user,clock_act=clock_act)

@app.route("/user")
def home1():
    return "timesheet.html"

@app.route("/")
def home2():
    return render_template("clock_land.html")

@app.route("/clockland")
def clockland():
    return render_template("clock_land.html")


@app.route("/clock")
def clock():
    clock_data = query_db()
    print('Quering DB', file=sys.stdout)
    return render_template("clock.html",clock_data=clock_data)


@app.route("/clocktable",  methods=['GET','POST'])
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
def clockthanks():
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

   

def query_db():
    conn,c = mysql_conn()
    logging.info("Hello in query_db")
    c.execute(f"""select  (@row_number:=@row_number + 1) AS a,week_id,start_date,end_date,hours_clocked,status,clock_id from clock,(SELECT @row_number:=0) AS temp order by start_date desc""")
    clock_det = c.fetchall()
    app.logger.info(clock_det)
    c.close()
    conn.close()
    return clock_det

def query_emp_db(empid):
    conn,c = mysql_conn()
    logging.info("Hello in employee user db")
    c.execute(f"""select employee_id,CONCAT(SURNAME,GIVEN_NAME) Name from emp.employee where employee_id ={empid}""")
    clock_user = c.fetchall()
    app.logger.info(clock_user)
    c.close()
    conn.close()
    return clock_user


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
