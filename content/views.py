from flask import Blueprint, current_app, render_template_string, render_template

# Create a Blueprint named 'content' for the content module
content_bp = Blueprint("content", __name__)

# Define the target domain for validation
TARGET_DOMAIN = 'yourdomain.com'

# Define a route to get and render templates
@content_bp.route("/<template_name>")
def render_template_from_db(template_name):
    """
    Fetches and renders a template only if it belongs to a parent 
    node matching the target domain.
    """
    driver = current_app.config["neo4j_driver"]
    
    # Updated query to enforce the domain relationship
    query = """
    MATCH (parent:Domain)-[:HAS_TEMPLATE]->(template:TEMPLATE {name: $name})
    WHERE parent.domain CONTAINS $domain
    RETURN REPLACE(template.content, '\\n', '\n') AS content
    """
    
    with driver.session() as session:
        result = session.run(query, name=template_name, domain=TARGET_DOMAIN)
        template_record = result.single()
        
        if template_record:
            template_content = template_record["content"]
            return render_template_string(template_content)
            
        return "Template not found or domain unauthorized.", 404

@content_bp.route('/')
def index():
    """
    Renders the 'home' template associated with the target domain.
    """
    driver = current_app.config["neo4j_driver"]
    
    # Query specifically for 'home' linked to the correct domain parent
    query = """
    MATCH (parent:Domain)-[:HAS_TEMPLATE]->(template:TEMPLATE {name: 'home'})
    WHERE parent.domain CONTAINS $domain
    RETURN REPLACE(template.content, '\\n', '\n') AS content
    """
    
    with driver.session() as session:
        result = session.run(query, domain=TARGET_DOMAIN)
        template_record = result.single()
        
        if template_record:
            template_content = template_record["content"]
            return render_template_string(template_content)
            
        return "Home page template not found or domain unauthorized.", 404