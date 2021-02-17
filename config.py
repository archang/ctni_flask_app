import os

S3_BUCKET                 = "ctni-bucket"
S3_KEY                    = "AKIAZWXEAQFW73KBCSMO"
S3_SECRET                 = "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"
S3_LOCATION               = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

SECRET_KEY                = os.urandom(32)
DEBUG                     = True
PORT                      = 5000
