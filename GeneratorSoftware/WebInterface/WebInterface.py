
'''
Close open socket: killall Python

'''
from time import sleep
from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit, send
from math import sqrt

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate')
def generate():
    def g():
    	yield '\nGenerating...\n'
    	yield 'some...\n'
    	yield 'digits...\n'
        for i in range(5):
            yield str(i) + '\n'
            sleep(1)
        yield 'DONE!\n'
    return app.response_class(g(), mimetype='text/plain')


# run it
if __name__ == '__main__':
	socketio.run(app)
