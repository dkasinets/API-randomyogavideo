import flask
from flask import request
from html_parser.get_urls import get_selenium_driver, get_urls
import json
import platform
from flask_cors import CORS, cross_origin


app = flask.Flask(__name__)


# Ex: http://127.0.0.1:8000/api-yt-links/?query=exercise+5min+easy
@app.route('/api-yt-links/', methods=['GET'])
@cross_origin()
def home():
    try:
        driver = get_selenium_driver()
        query = request.args['query']
        if query:
            urls = get_urls(query, driver)
            status = "success"
            status_msg = ""
        else:
            # Error placeholder video Quick Beginner Yoga
            urls = ["mawx7ROXv9o"]
            status = "error"
            status_msg = "Query string is empty or None"
        # Close all browser windows and end driver's session/process. (we have the link id)
        driver.quit()
        return json.dumps({ "query": query, "urls": urls, "platform": platform.system(), "status": status, "status_msg": status_msg})
    except Exception as e:
        # Close driver anyway
        driver.quit()
        # Error placeholder video Quick Beginner Yoga
        return json.dumps({ "query": query, "urls": ["mawx7ROXv9o"], "platform": platform.system(), "status": "error", "status_msg": f'Error: ({e}).'}) 
