import os, json
from flask import flash, redirect, render_template, request, session, url_for, abort
from boto3.session import Session 
from vodPlatform import app, private_ip, public_ip, port


@app.route('/index')
def index():
    # return render_template('login.html')
    access_key = session.get('access_key')
    secret_key = session.get('secret_key')
    try:
        assert(access_key!=None and secret_key!=None)
        client = Session(access_key, secret_key).client('s3', endpoint_url = f"http://{public_ip}:{port}")
        return render_template('index.html', client=client)
    except AssertionError:
        abort(401)


@app.route('/video')
def video_page():
    video_id = request.args.get('vid')
    access_key = session.get('access_key')
    secret_key = session.get('secret_key')
    try:
        assert(access_key!=None and secret_key!=None)
        client = Session(access_key, secret_key).client('s3', endpoint_url = f"http://{public_ip}:{port}")
        meta_data=client.head_object(Bucket="videos", Key=video_id)["Metadata"]
        src_url=client.generate_presigned_url("get_object", Params={"Bucket": "videos", "Key": video_id})
        return render_template('video.html', meta_data=meta_data, src_url=src_url)
    except AssertionError:
        abort(401)
    except Exception:
        abort(404)
    

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        access_key = request.form['access_key']
        secret_key = request.form['secret_key']

        try:
            client = Session(access_key, secret_key).client('s3', endpoint_url = f"http://{private_ip}:{port}")
            client.list_buckets()
            session['access_key'] = access_key
            session['secret_key'] = secret_key
            session['endpoint_url'] = f"http://{private_ip}:{port}"
            session['host'] = f"http://{public_ip}:{port}"
            return redirect(url_for('index'))
        except Exception:
            flash('Invalid keys!')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        access_key = request.form['access_key']
        secret_key = request.form['secret_key']
        resecret_key = request.form['resecret_key']
        
        if secret_key != resecret_key:
            flash('Inconsistent secret key!')
            return redirect(url_for('register'))

        user_list = json.load(os.popen("radosgw-admin metadata list user"))

        if access_key not in user_list:
            os.popen(f"radosgw-admin user create --uid={access_key} --display-name={access_key} --access_key={access_key} --secret={secret_key}")
            session['access_key'] = access_key
            session['secret_key'] = secret_key
            session['endpoint_url'] = f"http://{private_ip}:{port}"
            session['host'] = f"http://{public_ip}:{port}"
            return redirect(url_for('index'))
        else:
            flash('Access key already used!')
            return redirect(url_for('register'))

    return render_template('register.html')
