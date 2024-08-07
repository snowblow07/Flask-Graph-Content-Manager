from flask import Blueprint, render_template, redirect, current_app, request, url_for
from auth.models import login_required
from datetime import datetime
from content.views import TARGET_DOMAIN

# Create a Blueprint named "blog" for the blog module
blog_bp = Blueprint("blog", __name__)

@blog_bp.route('/templates')
@login_required
def get_templates():
    driver = current_app.config["neo4j_driver"]
    with driver.session() as session:
        # MODIFICACIÓN: Añadido label :Domain para filtrar correctamente
        result = session.run(
            """
            MATCH (parent:Domain)-[:HAS_TEMPLATE]->(t:TEMPLATE)
            WHERE parent.domain CONTAINS $domain
            RETURN t
            """,
            domain=TARGET_DOMAIN
        )
        templates = [record['t'] for record in result]
    return render_template('templates.html', templates=templates)

@blog_bp.route('/update/<int:node_id>', methods=['GET', 'POST'])
@login_required
def update_node(node_id):
    driver = current_app.config["neo4j_driver"]

    if request.method == 'GET':
        with driver.session() as session:
            # MODIFICACIÓN: Añadido label :Domain
            result = session.run(
                """
                MATCH (parent:Domain)-[:HAS_TEMPLATE]->(n) 
                WHERE id(n) = $node_id 
                RETURN n.name AS name, REPLACE(n.content, '\\n', '\n') AS content,
                       n.loc AS loc, n.lastmod AS lastmod, n.changefreq AS changefreq, 
                       n.priority AS priority, parent.domain AS domain
                """,
                node_id=node_id
            )
            current_data = result.single()
            if not current_data:
                return "Node not found or has no domain relationship.", 404
        return render_template('update.html', node_id=node_id, current_data=current_data)

    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        base_url = request.form['base_url']
        url = request.form['url']
        domain = request.form.get('domain', TARGET_DOMAIN)

        loc = f"{base_url}{url}"
        lastmod = datetime.now().strftime("%Y-%m-%d")
        changefreq = "weekly"
        priority = "0.5"

        with driver.session() as session:
            # MODIFICACIÓN: Se añadió :Domain en el MERGE para asegurar que 
            # el nuevo padre tenga la etiqueta correcta si se crea uno nuevo.
            session.run(
                """
                MATCH (old_parent:Domain)-[r:HAS_TEMPLATE]->(n)
                WHERE id(n) = $node_id
                SET n.name = $name, n.content = $content, n.loc = $loc, 
                    n.lastmod = $lastmod, n.changefreq = $changefreq, n.priority = $priority
                
                WITH n, r, old_parent, $domain as new_domain_str
                WHERE old_parent.domain <> new_domain_str
                
                MERGE (new_parent:Domain {domain: new_domain_str})
                CREATE (new_parent)-[:HAS_TEMPLATE]->(n)
                DELETE r
                """,
                node_id=node_id, name=name, content=content, loc=loc, lastmod=lastmod, 
                changefreq=changefreq, priority=priority, domain=domain
            )
        return redirect(url_for('blog.get_templates'))

@blog_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_node():
    driver = current_app.config["neo4j_driver"]
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        base_url = request.form['base_url']
        url = request.form['url']

        loc = f"{base_url}{url}"
        lastmod = datetime.now().strftime("%Y-%m-%d")
        changefreq = "weekly"
        priority = "0.5"

        with driver.session() as session:
            # MODIFICACIÓN: Se añadió :Domain al MERGE. 
            # Esto evita que sheengreen.com se cree sin etiqueta.
            session.run(
                """
                MERGE (parent:Domain {domain: $domain})
                CREATE (parent)-[:HAS_TEMPLATE]->(n:TEMPLATE {
                    name: $name, content: $content, loc: $loc, 
                    lastmod: $lastmod, changefreq: $changefreq, priority: $priority
                })
                """,
                domain=TARGET_DOMAIN, name=name, content=content, loc=loc, 
                lastmod=lastmod, changefreq=changefreq, priority=priority
            )
        return redirect(url_for('blog.get_templates'))
    return render_template('create.html')

@blog_bp.route('/delete/<int:node_id>')
@login_required
def delete_node(node_id):
    driver = current_app.config["neo4j_driver"]
    with driver.session() as session:
        # MODIFICACIÓN: Añadido label :TEMPLATE por seguridad
        session.run(
            "MATCH (n:TEMPLATE) WHERE id(n) = $node_id DETACH DELETE n", node_id=node_id
        )
    return redirect(url_for('blog.get_templates'))