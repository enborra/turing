from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', methods=['GET'])
def route_index():
    return render_template('index.htm')


app.run(
    debug=True,
    host='0.0.0.0',
    port=5000,
)
