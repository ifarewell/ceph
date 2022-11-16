import click
from boto3.session import Session
from vodPlatform import app, private_ip, port


def clean_bucket(client, bucket_name):
    resp = client.list_objects(Bucket=bucket_name)
    assert resp["Name"] == bucket_name
    for obj in resp.get("Contents", []):
        key = obj["Key"]
        client.delete_object(Bucket=bucket_name, Key=key)
        click.echo(f"Object {key} deleted!")

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def init(drop):
    """Initialize the database."""
    access_key = 'admin'
    secret_key = 'admin'

    session = Session(access_key, secret_key)
    client = session.client("s3", endpoint_url=f"http://{private_ip}:{port}")
    if drop:
        for bucket in client.list_buckets()["Buckets"]:
            bucket_name = bucket["Name"]
            if bucket_name in ["images", "videos"]:
                clean_bucket(client, bucket_name)
                client.delete_bucket(Bucket=bucket_name)
        click.echo("All buckets deleted!")
    for bucket_name in ["images", "videos"]:
        client.create_bucket(Bucket=bucket_name, ACL="public-read-write")
    click.echo("New buckets created!")


@app.cli.command()
def forge():
    """Generate fake data."""

    access_key = 'admin'
    secret_key = 'admin'

    session = Session(access_key, secret_key)
    client = session.client("s3", endpoint_url=f"http://{private_ip}:{port}")

    videos = [
        {'title': 'Programming Thoughts and Methods', 'publish_time': '2017-12-03 20:37:00', 'subject': 'Computer Science', 'publisher': 'Alice'},
        {'title': 'Python Program Design', 'publish_time': '2018-11-25 15:12:30', 'subject': 'Computer Science', 'publisher': 'Bob'},
        {'title': 'Calculus', 'publish_time': '2015-08-25 08:15:30', 'subject': 'Mathematics', 'publisher': 'Mary'},
        {'title': 'Principles of Education', 'publish_time': '2020-08-12 20:15:36', 'subject': 'Education', 'publisher': 'Steve'},
        {'title': 'Psychological Development and Education', 'publish_time': '2021-09-16 18:45:30', 'subject': 'Education', 'publisher': 'Joseph'},
        {'title': 'Macroeconomics', 'publish_time': '2016-06-17 09:35:20', 'subject': 'Economy', 'publisher': 'Paul'},
        {'title': 'Theoretical Mechanics', 'publish_time': '2009-07-04 09:18:58', 'subject': 'Physics', 'publisher': 'Elsa'},
        {'title': 'Art Theory for Film and Television', 'publish_time': '2014-02-20 06:29:57', 'subject': 'Film and Television', 'publisher': 'Tim'},
        {'title': 'Contemporary Literature', 'publish_time': '2013-01-28 16:58:58', 'subject': 'Literature', 'publisher': 'Tom'},
        {'title': 'Criminal Law', 'publish_time': '2012-07-25 23:30:30', 'subject': 'Law', 'publisher': 'Frank'},
    ]

    vprefix='./videos/'
    iprefix='./frontPages/'

    for v in videos:
        client.put_object(
            Bucket = "videos",
            Key = v["title"],
            ACL = "authenticated-read",
            Metadata = v,
            Body = open(vprefix+v['title']+'.mp4', "rb").read()
        )
        client.put_object(
            Bucket = "images",
            Key = v["title"],
            ACL = "public-read",
            Body = open(iprefix+v['title']+'.png', "rb").read()
        )
        click.echo(f"Object {v['title']} added!")
    click.echo('Done.')
