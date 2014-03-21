from flask import Flask
from flask import abort, escape, make_response, redirect, render_template, request, session, url_for

import json
from datetime import datetime

LISTENING_INTERFACE = '0.0.0.0'
LISTENING_PORT='5000'

app = Flask(__name__)
app.debug = True

#db = SQLAlchemy(app)

@app.route('/')
@app.route('/index.html', methods=['GET'])
def index():
    return render_template('index.html', title='testhost', date=datetime.utcnow())

@app.route('/home')
def home():
    return redirect(url_for('index'))

@app.route('/test/post', methods=['GET', 'POST'])
def test_post():
    if request.method == 'POST':
        if 'application/json' in request.content_type:
            return json.jsonify(status='ok')
        else:
            return 'ok'
    else:
        return 'Expected POST, received {0}'.format(request.method)

@app.route('/test/<int:test_int>')
def show_int(test_int):
    return '%d' % test_int

@app.route('/session')
def check_session():
    if 'status' in session:
        return 'session is %s' % escape(session['status'])
    return redirect(url_for('index'))

@app.route('/status')
def status():
    return 'ok'

@app.route('/delay/<delay>')
def delay(delay=1.0):
    import time
    time.sleep(float(delay))
    return 'ok'

@app.route('/unauthorized')
def protected():
    abort(401)

@app.route('/notfound')
def not_found():
    return '404', 404

@app.route('/cookie/set/<key>/<value>')
def set_cookie(key, value):
    response = make_response('', 200)
    response.set_cookie(key, value)
    return response

@app.route('/cookie/get/<key>')
def get_cookie(key):
    cookie_key = request.cookies.get(key)
    return make_response('{0}'.format(cookie_key), 200)

@app.route('/cookie/dump')
def dump_cookies():
    all_cookies = request.cookies
    return make_response('%s' % all_cookies)

@app.route('/headers')
def headers():
    response = make_response('see headers', 200)
    response.headers['datetime'] = datetime.utcnow()
    return response

#with app.test_request_context():
#    print url_for('return_delay', delay=2.0)
#    print url_for('static', filename='main.css')

with app.test_request_context('/test/post', method='POST'):
    assert request.path == '/test/post'
    assert request.method == 'POST'

#with app.request_context(environ) #pass a complete WSGI env


if __name__ == '__main__':
    #run the host on all interfaces
    app.run(host=LISTENING_INTERFACE, port=int(LISTENING_PORT))

