#!/usr/bin/env python
import os
from app import create_app
from gevent.wsgi import WSGIServer

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':    
    server = WSGIServer(('', 5000), app)
    server.serve_forever()
