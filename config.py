import os

S3_BUCKET                 = "ctni-bucket"
S3_KEY                    = "AKIAJGJ66THUJEQSKZXQ"
S3_SECRET                 = "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"
S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY                = os.urandom(32)
DEBUG                     = True
PORT                      = 5000