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
## show studies:
# 1) belonging to group that user is also a part of
# 2) that have been explicitly shared with email address of user logged in (via auth0)

def get_studies_scans():
    cur=conn.cursor()

    cur.execute( """
(select u.studies_id, u.studies_description, u.studies_name, u.studies_rating, u.studies_comments, s.Scan_ID,
    s.Scan_Name, s.Scan_Time, s.FOV, s.Echotime, s.Repetitiontime, s.Nrepetition, s.SpatResol,
    s.SliceThick, s.NSlice, s.SliceGap, s.SliceDistance, s.SliceOrient from studies u
    inner join scan s on u.studies_id = s.Study_ID
	where u.studies_id IN (
		(select users_studies.studies_id from users_studies where users_studies.users_id = 
			(select users.users_id from users where users.users_email = 'yoyashoza@gmail.com'))
        UNION
        (select studies_groups.studies_id from studies_groups where studies_groups.groups_id = 
			(select users_groups.groups_id from users_groups where users_groups.users_id = 
				(select users.users_id from users where users.users_email = 'yoyashoza@gmail.com')))))
    """)


    account = cur.fetchall()
    return account
def get_groups():
    cur = conn.cursor()
    cur.execute("SELECT  groups_name FROM grps")
    account = cur.fetchall()
    return account

def get_user_id_from_email(email):
    cur=conn.cursor()
    emailgrabbed=email
    cur.execute("select u.users_id from users u WHERE u.users_email = '%s'" % emailgrabbed)
    account = cur.fetchall()
    return account

def update_user_studies_from_email(user_id,names):
    cur = conn.cursor()
    print("hhhhh",names)
    for nameg in names:
        print("q",nameg)
        namei=int(nameg)
        print("qq",type(user_id))
        cur.execute("INSERT INTO users_studies (users_id,studies_id) VALUES  (%i,%i)" % (user_id,namei))
    conn.commit()

def get_user_groupid_from_UG(usergroup_string):
    cur=conn.cursor()
    UGgrabbed=usergroup_string
    cur.execute("select g.groups_id from grps g WHERE g.groups_name = '%s'" % UGgrabbed)
    account = cur.fetchall()
    return account

def update_UG_studies_from_UG(UGid,names):
    cur = conn.cursor()
    for nameg in names:
        print("q",nameg)
        namei=int(nameg)
        print("qq",type(UGid))
        cur.execute("INSERT INTO studies_groups (groups_id,studies_id) VALUES  (%i,%i)" % (UGid,namei))
    conn.commit()




