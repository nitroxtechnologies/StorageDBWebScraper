#!/usr/bin/env python
import pymysql
from login import host, pwd, user, db
conn = pymysql.connect(host=host,port=3306, user=user, passwd=pwd, db=db)

cur = conn.cursor()

# cur.execute("SELECt TABLE URLs (URL TEXT)")
cur.execute("SELECT * FROM URLs")

# print(cur.description)

# print()

with open('facilities', 'w') as out:
    for row in cur:
        out.write(row[0] + "\n")
    out.close()

cur.close()
conn.close()
