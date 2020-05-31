import os
from flask import Flask, request, redirect, url_for, render_template, jsonify
import json
from flask_cors import CORS, cross_origin
import parser
import article_credibility

app = Flask(__name__)
cors = CORS(app)

@app.route('/api', methods = ['GET', 'POST'])
@cross_origin()
def article_check():
    if request.method == 'POST':
        url = request.form.get('article_url')
        if url is not None:
            article = parser.Strip(url)
            if article.is_success():
                data = {}
                data['text'] = article.html_text()
                data['title'] = article.article_title()
                reliable(article.raw_text())
                return jsonify(data)
            else:
                return "ERROR"
        else:
            return "didn't get an article url"
    else:
        return redirect('https://google.com') # this will be the url of our pretty home page 
        # hopefully? or maybe redirect to extension

@app.route('/')
@cross_origin()
def home():
    # either gonna display a home page where you can upload an article URL yourself, or take you to the chrome extension
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', threaded = True)
