import sqllite3

conn = sqllite3.connect('clock.db')
c = conn.cursor()

c.execute(""" create table clock_details( id integer primary key autoincrement,week_name text ,emp_name text, description text)""")
c.execute(""" Insert into clock_details (weekname , emp_name, description) values
              ('WK1', 'Thulasi' , 'Please approve'),
              ('WK2','Hemsagar', 'Worked hard'),
              ('WK3','Saanvi','Cool Work')""")

conn.commit()
conn.close()
