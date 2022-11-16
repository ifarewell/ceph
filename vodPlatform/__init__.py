from flask import Flask, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vodPlatform'
public_ip = "81.68.255.144"
private_ip = "172.17.0.12"
port = "7480"


@app.context_processor
def inject_user():
    return dict(session=session)


from vodPlatform import views, errors, commands