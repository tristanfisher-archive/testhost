from flask import Flask
from flask import url_for, request

import json

LISTENING_INTERFACE = '0.0.0.0'
LISTENING_PORT='5000'

app = Flask(__name__)
app.debug = True

#db = SQLAlchemy(app)

@app.route('/')
@app.route('/index.html', methods=['GET'])
def index():
    return './'

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

@app.route('/status')
def status():
    return 'ok'

#URL_for functions.

@app.route('/delay/<delay>')
def delay(delay=1.0):
    import time
    time.sleep(float(delay))
    return 'ok'

#with app.test_request_context():
#    print url_for('return_delay', delay=2.0)


if __name__ == '__main__':
    #run the host on all interfaces
    app.run(host=LISTENING_INTERFACE, port=int(LISTENING_PORT))

