import boto3

s3 = boto3.client('s3')

resp = s3.create_bucket(Bucket='smangam19333',ACL='private')
print(resp)
