from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
import json

from database import db_bp, init_db
from content import content_bp
from auth import auth_bp
from blog import blog_bp
#from mktools import mktools_bp
#from tracking import tracking_bp
#from twilio import twilio_bp
from sitemap import sitemap_bp  # Import the sitemap blueprint
from sessions_management import sessions_bp  # Import the sessions blueprint

#Create a Flask application
app = Flask(__name__)

#Secret key for the Flask app
app.secret_key = 'your_secret_key'

#Initialize the database within the Flask app
init_db(app)

# Initialize Bcrypt with the Flask app
bcrypt = Bcrypt(app)

#Register the "auth", "blog", and "db", and more blueprints associating them with URL prefixes
app.register_blueprint(db_bp, url_prefix="/database")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(blog_bp, url_prefix="/blog")
app.register_blueprint(content_bp, url_prefix="/")
#app.register_blueprint(mktools_bp, url_prefix="/marketing")
#app.register_blueprint(tracking_bp, url_prefix="/tracking")
#app.register_blueprint(twilio_bp, url_prefix="/twilio")
app.register_blueprint(sitemap_bp, url_prefix="/")  # Register the sitemap blueprint
app.register_blueprint(sessions_bp, url_prefix="/sessions_management")  # Register the sessions blueprint

if __name__ == "__main__":
    #Run the Flask app in debug mode
    app.run(host='0.0.0.0', port='5050', debug=True)
