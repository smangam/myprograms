import boto3

s3 = boto3.client('s3')


resp = s3.list_objects(Bucket='sunilmangam.com')

for contents in resp['Contents']:
  print(contents['Key'])
