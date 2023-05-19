import json
import os
from flask import Flask, jsonify, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/dashboard')
def dashboard():
    data = [
        {'id': 112421, 'name': 'Alice', 'age': 25, 'location': 'California'},
        {'id': 234543, 'name': 'Bob', 'age': 30, 'location': 'Texas'},
        {'id': 334554, 'name': 'Charlie', 'age': 35, 'location': 'New York'},
        {'id': 445654, 'name': 'Dave', 'age': 40, 'location': 'Florida'}
    ]

    relationships = [
        {'source': 'Alice', 'target': 'Bob', 'relationship': 'FRIENDS'},
        {'source': 'Alice', 'target': 'Charlie', 'relationship': 'ENEMIES'},
        {'source': 'Bob', 'target': 'Dave', 'relationship': 'ENEMIES'}
    ]

    nodes = {}
    links = []
    for item in data:
        id = item['id']
        name = item['name']
        nodes[name] = {'id': id, 'name': name}

    for relationship in relationships:
        source = relationship['source']
        target = relationship['target']
        relationship_type = relationship['relationship']

        links.append(
            {'source': nodes[source]['id'], 'target': nodes[target]['id'], 'relationship': relationship_type}
        )

    data = {'nodes': list(nodes.values()), 'links': links}

    # Pass the data to the template for rendering
    return render_template('hello.jinja', data=json.dumps(data))

app.debug = True
app.run(host='0.0.0.0', port=4000)
