import boto3

s3 = boto3.client('s3')

resp = s3.list_buckets()

for bucket in resp['Buckets']:
  print(bucket['Name'])


for owner in resp['Owner']:
  print(owner)
