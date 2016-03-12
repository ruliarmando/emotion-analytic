from flask import Flask, request
from analytic.views import analytic

app = Flask(__name__)


@app.before_request
def option_autoreply():
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()
        
        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']
            
        h = resp.headers
        
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Mehthod']
        h['Access-Control-Max-Age'] = "10"
        
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers
            
        return resp
        

@app.after_request
def set_allow_origin(resp):
    h = resp.headers
    
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        
    return resp

app.config.from_object('configuration.DevelopmentConfig')
app.register_blueprint(analytic)