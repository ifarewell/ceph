import boto
import boto.s3.connection
host =  '172.17.0.12'
access_key = '6U9JEXSC9PBFPJIAH8U3'
secret_key = 'Ac9QUrzCmIMdVnpwvYTIZwfoztg0oHqqhnbMBAXf'
conn = boto.connect_s3(
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key,
    host =host, port=7480,
    is_secure=False,
    calling_format = boto.s3.connection.OrdinaryCallingFormat()
)
bucket = conn.create_bucket('py-first')
for bucket in conn.get_all_buckets():
    print("{name}\t{created}".format(name = bucket.name, created = bucket.creation_date))
