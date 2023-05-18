import json
import os
from flask import Flask, jsonify, render_template, request
from flask_bootstrap import Bootstrap
from neo4j import GraphDatabase

app = Flask(__name__)
bootstrap = Bootstrap(app)
driver = GraphDatabase.driver("bolt://3.86.162.148:7687", auth=("neo4j", "cannon-multiplication-meridian"))

def hello():
    data = [
        {'id': 112421, 'name': 'Alice', 'age': 25, 'location': 'California'},
        {'id': 234543, 'name': 'Bob', 'age': 30, 'location': 'Texas'},
        {'id': 334554, 'name': 'Charlie', 'age': 35, 'location': 'New York'},
        {'id': 445654, 'name': 'Dave', 'age': 40, 'location': 'Florida'}
    ]

    cypher_query = """
        UNWIND $data AS row
        MERGE (user:User {id: row.id})
        SET user.name = row.name, user.age = row.age, user.location = row.location
    """

    with driver.session() as session:
        session.run(cypher_query, data=data)

    cypher_relationship_query = """
        MATCH (alice:User {name: 'Alice'}), (bob:User {name: 'Bob'}),
              (charlie:User {name: 'Charlie'}), (dave:User {name: 'Dave'})
        MERGE (alice)-[:FRIENDS]->(bob)
        MERGE (alice)-[:ENEMIES]->(charlie)
        MERGE (bob)-[:ENEMIES]->(dave)
    """

    with driver.session() as session:
        session.run(cypher_relationship_query)


@app.route('/dashboard')
def dashboard():
    cypher_relationship_query = """
        MATCH (alice:User {name: 'Alice'})-[:FRIENDS]-(bob),
              (alice)-[:ENEMIES]-(charlie),
              (bob)-[:ENEMIES]-(dave)
        RETURN alice.name AS alice_name, bob.name AS bob_name,
               charlie.name AS charlie_name, dave.name AS dave_name
    """
    with driver.session() as session:
        result = session.run(cypher_relationship_query)

        relationships = [dict(record) for record in result]

        nodes = {}
        links = []
        for relationship in relationships:
            alice_name = relationship['alice_name']
            bob_name = relationship['bob_name']
            charlie_name = relationship['charlie_name']
            dave_name = relationship['dave_name']

            if alice_name not in nodes:
                nodes[alice_name] = {'id': len(nodes) + 1, 'name': alice_name}
            if bob_name not in nodes:
                nodes[bob_name] = {'id': len(nodes) + 1, 'name': bob_name}
            if charlie_name not in nodes:
                nodes[charlie_name] = {'id': len(nodes) + 1, 'name': charlie_name}
            if dave_name not in nodes:
                nodes[dave_name] = {'id': len(nodes) + 1, 'name': dave_name}

            links.append(
                {'source': nodes[alice_name]['id'], 'target': nodes[bob_name]['id'], 'relationship': 'FRIENDS'})
            links.append(
                {'source': nodes[alice_name]['id'], 'target': nodes[charlie_name]['id'], 'relationship': 'ENEMIES'})
            links.append({'source': nodes[bob_name]['id'], 'target': nodes[dave_name]['id'], 'relationship': 'ENEMIES'})

        data = {'nodes': list(nodes.values()), 'links': links}

    return render_template('hello.jinja', data=json.dumps(data))


app.debug = True
app.run(host='0.0.0.0', port=4000)
