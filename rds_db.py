import pymysql

conn = pymysql.connect(
    host='ctni.cmuad72yozvs.us-east-1.rds.amazonaws.com',
    port=3306,
    user='admin',
    password='Admin12345',
    db='ctni',

)

#insert query
def insert_account(User_ID,Username,Password,Role,Blocked):
    cur=conn.cursor()
    cur.execute("INSERT INTO account (User_ID,Username,Password,Role,Blocked) VALUES  (%s,%s,%s,%s,%s)", (User_ID,Username,Password,Role,Blocked))
    conn.commit()

#read the data
def get_account():
    cur=conn.cursor()
    cur.execute("SELECT *  FROM account")
    account = cur.fetchall()
    return account