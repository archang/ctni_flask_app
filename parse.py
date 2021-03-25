import sys
from config import conn


def methodFile(path_to_file):
    users_id = 2

    Scan_Name = " testname"
    Scan_Time = "10:28:18"
    FOV = " "
    Echotime = " "
    Repetitiontime = " "
    Nrepetition = " "
    SpatResol = " "
    SliceThick = " "
    NSlice = " "
    SliceGap = " "
    SliceDistance = " "
    SliceOrient = " "

    date_time = "$$ Sun Jan 01 00:00:00 2009 EST (UT-5h)  anonymous"

    studies_description = "testdesc "
    studies_comments = "testc "
    studies_name = "testn "
    studies_rating = 4


    print("here",file=sys.stderr)
    with open(path_to_file) as f:
        for line in f:
            if line.startswith("##OWNER="):
                date_time = f.readline()
            if line.startswith("##$PVM_SpatResol="):
                SpatResol = f.readline()
            if line.startswith("##$PVM_NRepetitions="):
                Nrepetition = str(line[20:])
            if line.startswith("##$PVM_SPackArrNSlices="):
                NSlice = f.readline()
            if line.startswith("##$PVM_SPackArrSliceOrient="):
                SliceOrient = f.readline()
            if line.startswith("##$PVM_EchoTime="):
                Echotime = str(line[16:])
            if line.startswith("##$PVM_RepetitionTime="):
                Repetitiontime = str(line[22:])
            if line.startswith("##$MultiRepetitionTime="):
                Repetitiontime = f.readline()
            if line.startswith("##$PVM_SliceThick="):
                SliceThick = str(line[18:])
            if line.startswith("##$PVM_SPackArrSliceGap="):
                SliceGap = f.readline()
            if line.startswith("##$PVM_SPackArrSliceDistance="):
                SliceDistance = f.readline()



    tuple1 = (studies_description, studies_comments, studies_name, studies_rating)

    cur = conn.cursor()

    cur.execute("""
    INSERT INTO studies (studies_description, studies_comments, studies_name, studies_rating)
    VALUES (%s, %s, %s, %s);
    """, tuple1)
    cur.execute("""
    SELECT studies_id from studies ORDER BY studies_id DESC limit 1;
    """)
    studies_id = cur.fetchone()[0]
    tuple2 = (Scan_Name, Scan_Time, FOV, Echotime, Repetitiontime, Nrepetition, SpatResol, SliceThick, NSlice, SliceGap, SliceDistance, studies_id, SliceOrient)

    cur.execute("""
    INSERT INTO scans (Scan_Name, Scan_Time, FOV, Echotime, Repetitiontime, Nrepetition, SpatResol, SliceThick, NSlice, SliceGap, SliceDistance, Study_ID, SliceOrient)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple2)

    tuple3 = (users_id,studies_id)
    cur.execute("""
    INSERT INTO users_studies (users_id, studies_id)
    VALUES (%s, %s)
    """, tuple3)
    conn.commit()
