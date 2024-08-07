from flask import Blueprint, Response, current_app
import xml.etree.ElementTree as ET

sitemap_bp = Blueprint('sitemap_bp', __name__)

def get_sitemap_data():
    driver = current_app.config["neo4j_driver"]
    query = """
    MATCH (n:TEMPLATE)
    RETURN n.name AS URL, n.changefreq AS changefreq, n.lastmod AS lastmod, n.loc AS loc, n.priority AS priority
    """
    with driver.session() as session:
        result = session.run(query)
        return result.data()

@sitemap_bp.route('/sitemap.xml')
def sitemap():
    data = get_sitemap_data()

    # Create the XML structure
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for entry in data:
        url = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url, "loc")
        loc.text = entry.get('loc', '')
        
        changefreq = ET.SubElement(url, "changefreq")
        changefreq.text = entry.get('changefreq', 'monthly')
        
        lastmod = ET.SubElement(url, "lastmod")
        lastmod.text = entry.get('lastmod', '')
        
        priority = ET.SubElement(url, "priority")
        priority.text = str(entry.get('priority', '0.5'))

    # Convert to a string with XML declaration
    xml_str = ET.tostring(urlset, encoding='utf-8', method='xml').decode('utf-8')
    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str

    response = Response(xml_str, mimetype='application/xml')
    return response
