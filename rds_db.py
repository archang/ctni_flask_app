from config import conn
from sqlalchemy.sql import text

#insert query
def insert_account(email, auth0id):
    cur = conn.cursor()
    results = cur.execute("SELECT * FROM users WHERE users_email = %s", (email))

    # new user will be added to the Users table in the database if not exist
    if results == 0:
        cur.execute("INSERT INTO users (auth0_id, users_email) VALUES  (%s,%s)", (auth0id, email))
        print("It Does Not Exist")
    else:
        print("User Exist")

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
## show studies belonging to user currently logged in (via auth0) as well as studies shared to current user
def get_studies_scans(email):
    print("get study scan called")
    cur=conn.cursor()


    getStudiesQuery = """
(select u.studies_id, u.studies_description, u.studies_name, u.studies_rating, u.studies_comments, s.Scan_ID,
    s.Scan_Name, s.Scan_Time, s.FOV, s.Echotime, s.Repetitiontime, s.Nrepetition, s.SpatResol,
    s.SliceThick, s.NSlice, s.SliceGap, s.SliceDistance, s.SliceOrient from studies u
    inner join scans s on u.studies_id = s.Study_ID
	where u.studies_id IN (
		(select users_studies.studies_id from users_studies where users_studies.users_id = 
			(select users.users_id from users where users.users_email = %s))
        UNION
        (select studies_groups.studies_id from studies_groups where studies_groups.groups_id = 
			(select users_groups.groups_id from users_groups where users_groups.users_id = 
				(select users.users_id from users where users.users_email = %s)))))
    """

    data1 = (email, email)
    cur.execute(getStudiesQuery, data1)


    account = cur.fetchall()
    print("Account", account)
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
