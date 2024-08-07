from flask import Blueprint, render_template, jsonify, redirect, current_app, request, url_for
from auth.models import login_required
from datetime import datetime
import ast
import json
import pytz

#create a Blueprint named "blog" for the blog module
sessions_bp = Blueprint("sessions_management", __name__)

def format_timestamp(timestamp):
    dt = datetime.fromisoformat(timestamp).replace(tzinfo=pytz.UTC)
    local_tz = pytz.timezone("America/New_York")
    dt_local = dt.astimezone(local_tz)
    return dt_local.strftime("%m-%d-%Y %H:%M")

def get_sessions():
    driver = current_app.config["neo4j_driver"]
    with driver.session() as session:
        result = session.run("MATCH (n:SESSION) RETURN n")
        sessions = []

        for record in result:
            node = record["n"]
            properties = node._properties
            history = properties.get("history", [])

            # Parse and sort history by timestamp
            history = [json.loads(entry) for entry in history]
            history.sort(key=lambda x: datetime.fromisoformat(x.get("timestamp", "1970-01-01T00:00:00")).replace(tzinfo=pytz.UTC), reverse=True)

            # Format history entries with timestamp
            for entry in history:
                entry["formatted_timestamp"] = format_timestamp(entry.get("timestamp", "1970-01-01T00:00:00"))

            # Extract latest interaction
            if history:
                latest_interaction = history[0]
                properties["latest_ip"] = latest_interaction.get("ip", "N/A")
                properties["latest_timestamp"] = latest_interaction.get("timestamp", "1970-01-01T00:00:00")
            else:
                properties["latest_ip"] = "N/A"
                properties["latest_timestamp"] = "1970-01-01T00:00:00"

            sessions.append({
                "n": {
                    "identity": node.id,
                    "labels": list(node.labels),
                    "properties": properties,
                    "elementId": node.element_id,
                    "history": history  # Ensure history is included in the session data
                }
            })

        # Sort sessions by latest_timestamp
        sessions.sort(key=lambda x: datetime.fromisoformat(x["n"]["properties"].get("latest_timestamp", "1970-01-01T00:00:00")).replace(tzinfo=pytz.UTC), reverse=True)

        # Convert timestamps to human-readable format for display
        for session in sessions:
            session["n"]["properties"]["latest_timestamp"] = format_timestamp(session["n"]["properties"]["latest_timestamp"])

        return sessions


def get_session_details(identity):
    driver = current_app.config["neo4j_driver"]
    with driver.session() as session:
        result = session.run("MATCH (n:SESSION) WHERE id(n) = $id RETURN n", id=identity)
        node = result.single()["n"]
        properties = node._properties
        
        # Ensure history is parsed correctly
        if "history" in properties:
            properties["history"] = [json.loads(entry) for entry in properties["history"]]
            
            # Sort history by timestamp
            properties["history"].sort(key=lambda x: datetime.fromisoformat(x.get("timestamp", "1970-01-01T00:00:00")).replace(tzinfo=pytz.UTC))
            
            # Format history entries with timestamp
            for entry in properties["history"]:
                entry["formatted_timestamp"] = format_timestamp(entry.get("timestamp", "1970-01-01T00:00:00"))
                
        return {
            "identity": node.id,
            "labels": list(node.labels),
            "properties": properties,
            "elementId": node.element_id
        }

@sessions_bp.route('/api/sessions', methods=['GET'])
@login_required
def api_sessions():
    sessions = get_sessions()
    return jsonify(sessions)

@sessions_bp.route('/api/sessions/<int:identity>', methods=['GET'])
@login_required
def api_session_details(identity):
    session_details = get_session_details(identity)
    return jsonify(session_details)

@sessions_bp.route('/')
@login_required
def index():
    sessions = get_sessions()
    return render_template('list_of_sessions.html', sessions=sessions)

@sessions_bp.route('/session/<int:identity>')
@login_required
def session_details(identity):
    session_details = get_session_details(identity)
    return render_template('session_detail.html', session=session_details)
