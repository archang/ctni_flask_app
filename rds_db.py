from config import conn


# insert query
def insert_account(User_ID, Username, Password, Role, Blocked):
    cur = conn.cursor()
    cur.execute("INSERT INTO account (User_ID,Username,Password,Role,Blocked) VALUES  (%s,%s,%s,%s,%s)",
                (User_ID, Username, Password, Role, Blocked))
    conn.commit()


# read the data
def get_account():
    cur = conn.cursor()
    cur.execute("SELECT *  FROM account")
    account = cur.fetchall()
    return account

def get_groups():
    cur = conn.cursor()

    cur.execute("""
    select groups_name from grps
    """)

    return cur.fetchall()

# /studies
## show studies:
# 1) belonging to group that user is also a part of
# 2) that have been explicitly shared with email address of user logged in (via auth0)

def get_studies_scans():
    cur = conn.cursor()

    cur.execute("""
    (select u.studies_id, u.studies_description, u.studies_name, u.studies_rating, u.studies_comments, s.Scan_ID,
        s.Scan_Name, s.Scan_Time, s.FOV, s.Echotime, s.Repetitiontime, s.Nrepetition, s.SpatResol,
        s.SliceThick, s.NSlice, s.SliceGap, s.SliceDistance, s.SliceOrient from studies u
    inner join scans s on u.studies_id = s.Study_ID
	where u.studies_id IN (
		(select users_studies.studies_id from users_studies where users_studies.users_id = 
			(select users.users_id from users where users.users_email = 'ahuja.b@northeastern.edu'))
        UNION
        (select studies_groups.studies_id from studies_groups where studies_groups.groups_id = 
			(select users_groups.groups_id from users_groups where users_groups.users_id = 
				(select users.users_id from users where users.users_email = 'ahuja.b@northeastern.edu')))))
    """)

    account = cur.fetchall()
    return account
