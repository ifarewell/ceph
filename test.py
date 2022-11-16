from boto3.session import Session

host = "http://172.17.0.12:7480"
access_key = '6U9JEXSC9PBFPJIAH8U3'
secret_key = 'Ac9QUrzCmIMdVnpwvYTIZwfoztg0oHqqhnbMBAXf'
# access_key = 'test1'
# secret_key = 'test1'

session = Session(access_key, secret_key)
client = session.client("s3", endpoint_url=host)

def empty_bucket(client, bucket_name):
    resp = client.list_objects(Bucket=bucket_name)
    assert resp["Name"] == bucket_name
    for obj in resp.get("Contents", []):
        key = obj["Key"]
        client.delete_object(Bucket=bucket_name, Key=key)
        print(f"DELETE Object {key}")

for bucket in client.list_buckets()["Buckets"]:
    bucket_name = bucket["Name"]
    if bucket_name in ["images", "videos"]:
        empty_bucket(client, bucket_name)
        resp = client.delete_bucket(Bucket=bucket_name)
print("Delete all buckets")

for bucket_name in ["images", "videos"]:
    resp = client.create_bucket(Bucket=bucket_name, ACL="public-read")
print("Create new buckets")

# APIS
## bucket API
"""
# create bucket
# ACL in ["private", "public-read", "public-read-write", "authenticated-read"]
res = client.create_bucket(Bucket="", ACL="public-read")
# delete bucket
res = client.delete_bucket(Bucket="")
# list bucket
res = client.list_buckets(Bucket="")
bucket_list = [bucket["Name"] for bucket in client.list_buckets()["Buckets"]]
# bucket info
res = client.head_bucket(Bucket="")
"""

## object API
""" 
# get object of bucket
res = client.list_objects(Bucket="")
# delete object of bucket
res = client.delete_object(Bucket="", Key="")
# get bucket object
res = client.get_object(Bucket="", Key="")
# get bucket object metadata
res = client.head_object(Bucket="", Key="")
"""

## Get and Put object
"""
resp = client.put_object(
    Bucket = "videos",
    Key = "video1",
    ACL = "public-read",
    Metadata = {"title": "Time-lapse SJTU", "desc": "Time-lapse photography of Shanghai Jiao Tong University landscape", "cover": "sjtu"},
    Body = open("../../video1.mp4", "rb").read()
)
resp = client.get_object(
    Bucket="",
    Key=""
)
with open('sjtu_download.flv', 'wb') as f:
    f.write(resp['Body'].read())
"""