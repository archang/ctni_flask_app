import pymysql
import sys

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
    cur.execute("INSERT INTO account (User_ID,Username,Password,Role,Blocked) VALUES  (%s,%s,%s,%s,%s)",
                (User_ID,Username,Password,Role,Blocked))
    conn.commit()

#read the data
def get_account():
    cur=conn.cursor()
    cur.execute("SELECT *  FROM account")
    account = cur.fetchall()
    return account

# /studies
## show studies belonging to user currently logged in (via auth0) as well as studies shared to current user
def get_studies_scans():
    cur=conn.cursor()

    cur.execute( """
    (select u.Study_ID, r.Owner, u.Study_Description, u.Study_Name, u.Study_Rating, u.Study_Comments, s.Scan_ID,
    s.Scan_Name, s.Scan_Time, s.FOV, s.Echotime, s.Repetitiontime, s.Nrepetition, s.SpatResol,
    s.SliceThick, s.NSlice, s.SliceGap, s.SliceDistance, s.SliceOrient from study u
    inner join scan s on u.Study_ID = s.Study_ID inner join registration r on u.Registration_ID = r.Registration_ID where r.Owner='lundbeck')
    UNION
    (select u.Study_ID, r.Owner, u.Study_Description, u.Study_Name, u.Study_Rating, u.Study_Comments, s.Scan_ID,
    s.Scan_Name, s.Scan_Time, s.FOV, s.Echotime, s.Repetitiontime, s.Nrepetition, s.SpatResol,
    s.SliceThick, s.NSlice, s.SliceGap, s.SliceDistance, s.SliceOrient from study u
    inner join registration r on u.Registration_ID = r.Registration_ID
    inner join scan s on u.Study_ID = s.Study_ID inner join shares on
    shares.study_id = u.Study_ID where shares.shared_with='lundbeck')
    """)

    account = cur.fetchall()
    return account

# /manage
# show only studies belonging to user currently logged in (via auth0)
# cur.execute("select columns from scan table join by study_ID with study table join by registration_ID select where owner=(auth0_email) ")
# def get_owned_studies():
#     cur = conn.cursor()
#     cur.execute("(select u.Study_ID, u.Study_Description, u.Study_Name, u.Study_Rating, u.Study_Comments, s.Scan_ID,"
#                 "s.Scan_Name, s.Scan_Time, s.FOV, s.Echotime, s.Repetitiontime, s.Nrepetition, s.SpatResol,"
#                 "s.SliceThick, s.NSlice, s.SliceGap, s.SliceDistance, s.SliceOrient from study u"
#                 "inner join scan s on u.Study_ID = s.Study_ID inner join registration r on u.Registration_ID = r.Registration_ID where r.Owner='lundbeck')"
# "UNION"
# "(select u.Study_ID, u.Study_Description, u.Study_Name, u.Study_Rating, u.Study_Comments, s.Scan_ID,"
#                 "s.Scan_Name, s.Scan_Time, s.FOV, s.Echotime, s.Repetitiontime, s.Nrepetition, s.SpatResol,"
#                 "s.SliceThick, s.NSlice, s.SliceGap, s.SliceDistance, s.SliceOrient from study u"
#                 "inner join scan s on u.Study_ID = s.Study_ID inner join shares on "
#                 "shares.study_id = u.Study_ID where shares.shared_with='lundbeck')")
