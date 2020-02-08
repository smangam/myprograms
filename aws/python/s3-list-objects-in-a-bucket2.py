import boto3
from botocore import UNSIGNED
from botocore.client import Config

s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))


resp = s3.list_objects(Bucket='sunilmangam.com')

for contents in resp['Contents']:
  print(contents['Key'])
