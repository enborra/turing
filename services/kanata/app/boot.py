from flask import Flask


app = Flask(__name__)


@app.route('/', methods=['GET'])
def route_index():
    return 'Hello, human!'


app.run(
    debug=True,
    host='0.0.0.0',
    port=5000,
)
