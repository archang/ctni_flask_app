from config import conn

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
    inner join scan s on u.Study_ID = s.Study_ID inner join share on
    share.Study_ID = u.Study_ID where share.shared_with='lundbeck')
    """)

    account = cur.fetchall()
    return account

