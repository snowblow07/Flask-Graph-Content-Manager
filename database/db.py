from flask import Blueprint, current_app
from neo4j import GraphDatabase

#create a Blueprint named "database" for the database module
db_bp = Blueprint("database", __name__)

#Neo4j database configuration
def init_db(app):
    NEO4J_URI = "neo4j+ssc://<your-db-id>.databases.neo4j.io"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "<your-password>"

#Neo4j local database configuration
#def init_db(app):
#    NEO4J_URI = "bolt://localhost" #Macports
#    NEO4J_URI = "bolt://localhost:7689" #Desktop App
#    NEO4J_USER = "neo4j"
#    NEO4J_PASSWORD = "<your-local-password>"

    #Create a driver for the Neo4j database
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    app.config["neo4j_driver"] = driver

# You can add more database-related routes and functionality here.
