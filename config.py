import os
import pymysql


conn = pymysql.connect(
    host='ctni.cmuad72yozvs.us-east-1.rds.amazonaws.com',
    port=3306,
    user='admin',
    password='Admin12345',
    db='ctni',
)

S3_BUCKET                 = "ctni-bucket"
S3_KEY                    = "AKIAZWXEAQFW42EJK3ZO"
S3_SECRET                 = "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"
S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY                = os.urandom(32)
DEBUG                     = True
PORT                      = 5000
