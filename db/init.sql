CREATE DATABASE emp;
use emp;

create table employee( employee_id integer primary key AUTO_INCREMENT, surname varchar(100),given_name varchar(100),location_id integer,start_date date,end_date date,manager_id integer,employee_type varchar(30),applicant_id integer,user_name varchar(8),email varchar(30),cognito_user varchar(1) DEFAULT 'N',user_confirmed varchar(1) DEFAULT 'N',email_confirmed varchar(1) DEFAULT 'N',cognito_msg varchar(250) DEFAULT '',create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);
ALTER TABLE employee AUTO_INCREMENT=1000;

create table employee_identity(employee_id integer, PAN VARCHAR(30),ADHAR VARCHAR(30),PASSPORT VARCHAR(30),DOB DATE,GENDER VARCHAR(1),create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

create table departments(department_id integer primary key AUTO_INCREMENT, NAME VARCHAR(30),description VARCHAR(150),BUDGET_CODE VARCHAR(30),create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

create table locations(location_id integer primary key AUTO_INCREMENT, location_code VARCHAR(30),description VARCHAR(150),address1 VARCHAR(300),PIN VARCHAR(30),STATE VARCHAR(30),COUNTRY VARCHAR(30),create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);


create table employee_positions(position_id integer primary key AUTO_INCREMENT, NAME VARCHAR(60),description VARCHAR(150),LEVEL integer,create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

create table employee_jobs(job_id integer primary key AUTO_INCREMENT,NAME VARCHAR(60),description VARCHAR(150),LOCATION_id integer,create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

create table employee_assignments(assignment_id integer primary key AUTO_INCREMENT,employee_id integer, position_id integer,job_id integer, supervisor_id integer,department_id integer,start_date date,end_date date,create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

create table emp_app_roles(user_name varchar(8),role_name varchar(15),start_date date,end_date date,create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

/*
insert into employee( surname,given_name ,location_id,start_date,end_date,manager_id,employee_type,applicant_id,user_name,email)values ('pathi','Chengalrayulu',1,'2022-01-01',null,2,'PERMANENT',0,null,'pathi.chengalrayulu@gmail.com'),
('LNU','Sandhya',1,'2022-01-01',null,1000,'PERMANENT',0,null,'a@gmail.com'),
('pathi','Mohan',1,'2022-01-01',null,1000,'PERMANENT',0,null,'b@gmail.com'),
('kandhati','Thulasi kumar',2,'2022-01-01',null,1000,'TEMPORARY',0,null,'kthulasikumar@gmail.com'),
('Mallavarapu','Supriya',2,'2022-01-01',null,1003,'TEMPORARY',0,null,'g@gmail.com');

insert into employee( surname,given_name ,location_id,start_date,end_date,manager_id,employee_type,applicant_id,user_name,email,cognito_user,user_confirmed, email_confirmed,cognito_msg) values
('kandhati','Hemsagar',1,'2022-06-01',null,1002,'TEMPORARY',0,null,'kthulasikumar@gmail.com','Y','Y','Y','User sysnced with cognito');


insert into locations(location_code,description,address1,PIN,STATE,COUNTRY) Values
('HEAD OFFICE','Head office','Rs.no. 208.1a ,surampalli village, Nuzvid Rd, Vijayawada','521212','Andhra Pradesh','India');

insert into departments(NAME,description,BUDGET_CODE) values
('Engineering','Core Team','01'),
('IT','Information Technology services','02');

insert into employee_positions(NAME,description,LEVEL) Values
('Manager','Manager',3),
('consultant','Consultant',5),
('Supervisor','Supervisor lead',4);

insert into employee_jobs(NAME,description,Location_id) Values
('Manager','Manager',1),
('consultant','Consultant',2),
('Supervisor','Supervisor lead',1);


insert into emp_app_roles(user_name,role_name,start_date,end_date) values
('A1000','AP101_ADMIN','2022-01-01',null);
insert into emp_app_roles(user_name,role_name,start_date,end_date) values
('A1001','AP101_USER','2022-01-01',null);
insert into emp_app_roles(user_name,role_name,start_date,end_date) values
('A1002','AP101_USER','2022-01-01',null);
insert into emp_app_roles(user_name,role_name,start_date,end_date) values
('A1003','AP101_USER','2022-01-01',null);
insert into emp_app_roles(user_name,role_name,start_date,end_date) values
('A1004','AP101_USER','2022-01-01',null);


UPDATE employee 
set user_name = concat('A',employee_id)
where user_name is null;
*/

CREATE DATABASE prj;
use prj;

create table projects(project_id integer primary key AUTO_INCREMENT,Project_name varchar(30),planned_start_date date,planned_end_date date,
actual_start_date date, actual_end_date date,description varchar(150),client_code varchar(30),project_mgr_id integer,currency varchar(3),create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

create table project_task(task_id integer primary key AUTO_INCREMENT,project_id integer,priority integer(2),short_name varchar(30), description varchar(150),planned_start_date date,planned_end_date date, actual_start_date date,actual_end_date date,planned_budget float(10,2),create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

/*
insert into projects(project_name,planned_start_date,planned_end_date,actual_start_date,actual_end_date,description,client_code,project_mgr_id,currency)values
('Clock App','2022-05-01','2022-07-30','2022-05-01',null,'Employee clocking App','TUL',1004,'INR');

insert into project_task(project_id,priority,description,planned_start_date,planned_end_date,actual_start_date,actual_end_date,planned_budget)
values(1,99,'Development','2022-05-01','2022-07-30','2022-05-01',null,100),
(1,99,'Testing','2022-07-01','2022-07-30','2022-07-01',null,100),
(1,99,'Unbillable','2022-07-01','2022-07-30','2022-07-01',null,100);;
*/




CREATE DATABASE clk;
use clk;

create table clock_activity( activity_id integer primary key AUTO_INCREMENT, activity_code varchar(30), short_name varchar(30), activity_desc varchar(150),start_date date,end_date date,employee_id integer,task_id integer,billable varchar(1),create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

create table clock(clock_id integer primary key AUTO_INCREMENT,week_id varchar(30), employee_id integer, start_date date,start_date_plus1 date,start_date_plus2 date,start_date_plus3 date,start_date_plus4 date,start_date_plus5 date,end_date date,hours_clocked integer,status varchar(30), submitted_date DATE,create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

create table clock_details(seq_no integer primary key AUTO_INCREMENT,clock_id integer ,activity_id integer, day1 integer,day2 integer,day3 integer,day4 integer,day5 integer, day6 integer,day7 integer,create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,update_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);

/*
insert into clock_activity(activity_code,activity_desc,start_date ,end_date ,employee_id ,task_id,billable) values ('Main project','primary work','2022-01-01','2023-01-01',1000,1,'Y'),('Holiday','company declared holiday','2022-01-01','2023-01-01',1000,2,'N'),('Sick Leave','Sick leave for less than 2 days','2022-01-01','2023-01-01',1000,3,'N'),('Side Project','Secondary assignment','2022-01-01','2023-01-01',1000,4,'Y'),('NotBill - HR','Non billable hr work','2022-01-01','2023-01-01',1000,5,'N'),('NotClocked','Not clocked yet','2022-01-01','2023-01-01',1000,6,'N');


insert into clock(week_id, employee_id, start_date,start_date_plus1,start_date_plus2 ,start_date_plus3 ,start_date_plus4 ,start_date_plus5,end_date, hours_clocked ,status,submitted_date)values ('wk22_02',1,'2022-01-03','2022-01-04','2022-01-05','2022-01-06','2022-01-07','2022-01-08','2022-01-09',0,'Submitted',CURRENT_DATE),('wk22_03',1,'2022-01-10','2022-01-11','2022-01-12','2022-01-13','2022-01-14','2022-01-15','2022-01-16',0,'Submitted',CURRENT_DATE),('wk22_04',1,'2022-01-17','2022-01-18','2022-01-19','2022-01-20','2022-01-21','2022-01-22','2022-01-23',0,'Submitted',CURRENT_DATE);
*/

DELIMITER &&;  
CREATE PROCEDURE get_clock_exists (INOUT var1 INTEGER,OUT var2 VARCHAR(100) )  
BEGIN 
      SELECT concat('wk',SUBSTR(YEARWEEK(SYSDATE()),3,2),'_',SUBSTR(YEARWEEK(SYSDATE()),5)) INTO var2;
      select count(1) INTO var1 from emp.employee where SYSDATE() BETWEEN start_date and end_date
      and employee_id = IFNULL(var1,1000);
      
END &&  
DELIMITER ;

DELIMITER &&;  
CREATE PROCEDURE insert_clock ( INOUT var1 INTEGER,IN var2  VARCHAR(100))  
BEGIN  
  DECLARE finished INTEGER DEFAULT 0;
  DECLARE l_cnt INTEGER DEFAULT 0;
  DECLARE eid INTEGER DEFAULT 0;
  DECLARE diff INTEGER DEFAULT 0;
  DECLARE curEmail 
		CURSOR FOR 
			 SELECT employee_id  FROM emp.employee e WHERE employee_id = IFNULL(var1,employee_id)
			 and SYSDATE() BETWEEN start_date and IFNULL(end_date,SYSDATE())
			 and exists (select 1 from emp.emp_app_roles r where role_name in ('AP101_ADMIN','AP101_USER')
                         and SYSDATE() BETWEEN start_date and IFNULL(end_date,SYSDATE()) and e.user_name = r.user_name) 
                         and not exists (select 1 from clk.clock where week_id = var2 and employee_id = IFNULL(var1,employee_id));
		DECLARE CONTINUE HANDLER 
        FOR NOT FOUND SET finished = 1;

			 	OPEN curEmail;
         select 'starting loop';
	       getEmail: LOOP
		       FETCH curEmail INTO eid;
		      	IF finished = 1 THEN 
			         LEAVE getEmail;
		        END IF;
		        select l_cnt + 1 into l_cnt;
		        SELECT WEEKDAY(SYSDATE()) INTO diff;
		        insert into clk.clock(week_id, employee_id, start_date,start_date_plus1,start_date_plus2 ,start_date_plus3 ,start_date_plus4 ,start_date_plus5,end_date, hours_clocked ,status,submitted_date)values 
            (var2,eid,DATE(DATE_ADD(SYSDATE() , INTERVAL (0-diff) DAY)),DATE(DATE_ADD(SYSDATE() , INTERVAL (1-diff) DAY)),DATE(DATE_ADD(SYSDATE() , INTERVAL (2-diff) DAY)),DATE(DATE_ADD(SYSDATE() , INTERVAL (3-diff) DAY)),DATE(DATE_ADD(SYSDATE() , INTERVAL (4-diff) DAY)),DATE(DATE_ADD(SYSDATE() , INTERVAL (5-diff) DAY)),DATE(DATE_ADD(SYSDATE() , INTERVAL (6-diff) DAY)),0,'Draft',CURRENT_DATE);
            
    	    END LOOP getEmail;
	      CLOSE curEmail;
	      set var1=l_cnt;
	    
	      
END &&  
DELIMITER ;   


DELIMITER &&;
CREATE PROCEDURE insert_clock_past ( INOUT var1 INTEGER,IN var3 DATE)
BEGIN
  DECLARE finished INTEGER DEFAULT 0;
  DECLARE l_cnt INTEGER DEFAULT 0;
  DECLARE eid INTEGER DEFAULT 0;
  DECLARE diff INTEGER DEFAULT 0;
  DECLARE var2 VARCHAR(10) DEFAULT 'wk22_36';
  DECLARE curEmail
                CURSOR FOR
                         SELECT employee_id  FROM emp.employee e WHERE employee_id = IFNULL(var1,employee_id)
                         and var3 BETWEEN start_date and IFNULL(end_date,SYSDATE())
                         and exists (select 1 from emp.emp_app_roles r where role_name in ('AP101_ADMIN','AP101_USER')
                         and var3 BETWEEN start_date and IFNULL(end_date,SYSDATE()) and e.user_name = r.user_name)
                         and not exists (select 1 from clk.clock where week_id = var2 and employee_id = IFNULL(var1,employee_id));
                DECLARE CONTINUE HANDLER
        FOR NOT FOUND SET finished = 1;
       SELECT concat('wk',SUBSTR(YEARWEEK(var3),3,2),'_',SUBSTR(YEARWEEK(var3),5)) INTO var2;
                                OPEN curEmail;
         select 'starting loop';
               getEmail: LOOP
                       FETCH curEmail INTO eid;
                        IF finished = 1 THEN
                                 LEAVE getEmail;
                        END IF;
                        select l_cnt + 1 into l_cnt;
                        SELECT WEEKDAY(SYSDATE()) INTO diff;
                        insert into clk.clock(week_id, employee_id, start_date,start_date_plus1,start_date_plus2 ,start_date_plus3 ,start_date_plus4 ,start_date_plus5,end_date, hours_clocked ,status,submitted_date)values
            (var2,eid,DATE(DATE_ADD(var3 , INTERVAL (0-diff) DAY)),DATE(DATE_ADD(var3 , INTERVAL (1-diff) DAY)),DATE(DATE_ADD(var3 , INTERVAL (2-diff) DAY)),DATE(DATE_ADD(var3 , INTERVAL (3-diff) DAY)),DATE(DATE_ADD(var3 , INTERVAL (4-diff) DAY)),DATE(DATE_ADD(var3 , INTERVAL (5-diff) DAY)),DATE(DATE_ADD(var3 , INTERVAL (6-diff) DAY)),0,'Draft',CURRENT_DATE);

            END LOOP getEmail;
              CLOSE curEmail;
              set var1=l_cnt;


END &&
DELIMITER ;


/*
set @wk =null;
set @empid =null;
CALL get_clock_exists(@empid, @wk);  
select @empid, @wk;

SET @M = null;  
CALL insert_clock(@M,@wk);  
SELECT @M; 

SET @M = null;
CALL insert_clock_past(@M,'2022-09-01');
SELECT @M;
SET @M = null;
CALL insert_clock_past(@M,SYSDATE());
SELECT @M;
*/

select * from clock;
