import flask
import time, math

app = flask.Flask(__name__)


@app.route('/')
def index():
    def inner():
        # simulates a long process which
        # we want to watch
        yield 'starting...<br>\n'
        for i in range(50):
            j = math.sqrt(i)
            time.sleep(.1)

            # this value should be inserted into
            # an HTML template
            yield str(i) + '<br/>\n'
        yield 'done!'
    return flask.Response(inner(), mimetype='text/html')

app.run(debug=True, port=5000, host='0.0.0.0')

