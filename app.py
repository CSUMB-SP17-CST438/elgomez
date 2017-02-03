import os
import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    var_1 = flask.request.args.get('var_1', "not set")
    var_2 = flask.request.args.get('var_2', "not set")
    return "1: " + var_1 + "; 2: " + var_2
    
app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080))
)
