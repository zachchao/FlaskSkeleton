import os
from dotenv import load_dotenv
if 'ENV' in os.environ and os.environ['ENV'] == 'prod':
  pass
else: # dev
  load_dotenv()

from flask import Flask
from flask import Flask, render_template, request, redirect, send_from_directory
from flask_talisman import Talisman
from flask_compress import Compress
from urllib.parse import urlparse, urlunparse

app = Flask(__name__)
Compress(app)

with app.app_context():
  # Controllers
  from controllers.dashboard_controller import dashboard_controller

# Cryptographically signs the session
app.secret_key = str.encode(os.environ['APP_SECRET_KEY'])
# Forces SSL
Talisman(app, content_security_policy=None)

app.register_blueprint(dashboard_controller, url_prefix='/dashboard')

@app.before_request
def redirect_nonwww():
  """Redirect non-www requests to www."""
  urlparts = urlparse(request.url)
  if urlparts.netloc == 'YOUR_SITE_NAME_HERE.com':
    urlparts_list = list(urlparts)
    urlparts_list[1] = 'www.YOUR_SITE_NAME_HERE.com'
    return redirect(urlunparse(urlparts_list), code=301)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/js/<path:path>')
def send_js(path):
  return send_from_directory('static/js', path, mimetype='text/javascript')

@app.route('/static/css/<path:path>')
def send_css(path):
  return send_from_directory('static/css', path, mimetype='text/css')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

