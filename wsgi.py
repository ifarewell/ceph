import os

from dotenv import load_dotenv
from gevent.pywsgi import WSGIServer

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from vodPlatform import app

if __name__=="__main__":
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
