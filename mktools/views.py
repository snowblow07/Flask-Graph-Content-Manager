from flask import Blueprint, render_template, request, jsonify
from tools.lighthouse import lighthouse

# Create a Blueprint named 'auth' for the authentication module
mktools_bp = Blueprint("mktools", __name__)

#Define a route for the mktools page
@mktools_bp.route("/mktools")
def seo_analize():
    return lighthouse("https://www.your-domain.com/")