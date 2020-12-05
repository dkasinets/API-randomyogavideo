import flask
from flask import request
from html_parser.get_urls import get_urls


app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    word = request.args['word']
    try:
        if word:
            urls = get_urls(word)
        return 'word=' + str(word) + " ||| " + str(urls)
    except KeyError:
        return f'Invalid input ({word})'
