import boto3

sts = boto3.client('sts')
s3 = boto3.resource('s3')

my_bucket = s3.bucket('sm100200')
my_bucket.create
