from flask import Blueprint, current_app, render_template, jsonify

# Create a Blueprint named 'tracking' for the tracking module
tracking_bp = Blueprint("tracking", __name__)

#Define a route fro the loging page
@tracking_bp.route("/login")
def login():
    return "Loging Page"

#Define a route for the logout page
@tracking_bp.route("/logout")
def logout():
    return "Logout Page"

@tracking_bp.route('/json/<string:string_id>')
def get_node_attributes(string_id):
    # Connect to the Neo4j database
    driver = current_app.config["neo4j_driver"]
    with driver.session() as session:
        # Write your Cypher query to retrieve node attributes using string_id
        cypher_query = (
            "MATCH (n:$string_id) RETURN n"
        )
        result = session.run(cypher_query, string_id=string_id)
        
        # Process the result to extract node attributes
        node_attributes = {}
        for record in result:
            node = record["n"]
            for key, value in node.items():
                node_attributes[key] = value
        
    return jsonify(node_attributes)

#Retrieve all attributes of a node and render a Jinja template
@tracking_bp.route('/workorder/<string:string_id>')
def render_work_order_template(string_id):
    # Connect to the Neo4j database
    driver = current_app.config["neo4j_driver"]
    with driver.session() as session:
        # Write your Cypher query to retrieve node attributes using string_id
        cypher_query = (
            "MATCH (n {name: $string_id}) RETURN n"
        )
        result = session.run(cypher_query, string_id=string_id)
        
        # Process the result to extract node attributes
        node_attributes = {}
        for record in result:
            node = record["n"]
            for key, value in node.items():
                node_attributes[key] = value

    # Render a Jinja template with node attributes
    return render_template("tracking.html", node=node_attributes)