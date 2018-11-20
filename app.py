import json
from flask import Flask
from flask import render_template, request


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

