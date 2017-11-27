from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def route_index(path):
    return render_template('app.htm')


app.run(
    debug=False,
    host='0.0.0.0',
    port=80,
)
