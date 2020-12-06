import flask
from flask import request
from html_parser.get_urls import get_urls
import json
import platform
from flask_cors import CORS, cross_origin


app = flask.Flask(__name__)


# Ex: http://127.0.0.1:8000/api-yt-links/?query=exercise+5min+easy
@app.route('/api-yt-links/', methods=['GET'])
@cross_origin()
def home():
    query = request.args['query']
    try:
        if query:
            urls = get_urls(query)
        else:
            urls = []
        return json.dumps({ "query": query, "urls": urls, "platform": platform.system(), "status": "success", "status_msg": ""})
    except Exception as e:
        return json.dumps({ "query": query, "urls": ["https://www.youtube.com/watch?v=lVehcuJXe6I"], "platform": platform.system(), "status": "error", "status_msg": f'Error: ({e}).'}) 
