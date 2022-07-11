import sqllite3

conn = sqllite3.connect('clock.db')
c = conn.cursor()

c.execute(""" select * from  clock_details""")

clock_det = c.fetchall()


conn.commit()
conn.close()
