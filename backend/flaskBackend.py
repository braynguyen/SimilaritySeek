from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os
import json
import linkedin_util

from embed import embed

app = Flask(__name__)
CORS(app)

@app.route('/')
def homepage():
    return render_template('index.html')

# Database connection settings
username = 'demo'
password = 'demo'
hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
port = '1972'
namespace = 'USER'
CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"


# Create SQLAlchemy engine
engine = create_engine(CONNECTION_STRING)


@app.route('/create', methods=['POST'])
def create():
    tableName = request.json.get('tableName')
    schema = "(row_id INTEGER PRIMARY KEY IDENTITY, Name VARCHAR(255), URL VARCHAR(255), About VARCHAR(255), Skills VARCHAR(255), Experiences VARCHAR(255), Interests VARCHAR(255), Education VARCHAR(255), vec VECTOR(DOUBLE, 384))"

    if not tableName:
        return jsonify({"response": "Table name is required"}), 400

    with engine.connect() as conn:
        try:
            with conn.begin() as trans:
                # Drop the table if it exists
                try:
                    conn.execute(text(f"DROP TABLE {tableName}"))
                except Exception:
                    pass  # Ignore error if the table doesn't exist

                # Create the table with the provided schema
                conn.execute(text(f"CREATE TABLE {tableName} {schema}"))

                trans.commit()  # Commit the transaction

        except Exception as inst:
            return jsonify({"response": str(inst)}), 400

    return jsonify({"response": "Table created successfully"}), 200


# Get all rows from a table
@app.route('/getall', methods=['POST'])
def getall():
    tableName = request.json.get('tableName')

    with engine.connect() as conn:
        try:
            # Execute the query to fetch all data from the table
            result = conn.execute(text(f"SELECT * FROM {tableName}"))
            # Get column names from the result
            columns = result.keys()

            # Convert rows into a list of dictionaries, zipping column names with each row's values
            data = [dict(zip(columns, row)) for row in result]
        except Exception as inst:
            return jsonify({"response": str(inst)}), 400

    return jsonify({"response": data}), 200

@app.route('/vectorFind/<int:rowId>/<int:n>', methods=['POST'])
def find(rowId, n):
    tableName = request.json.get('tableName')
    with engine.connect() as conn:
        try:
            result = conn.execute(text(f"SELECT * FROM {tableName}"))
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result]
            vec = None
            for d in data:
                if d['row_id'] == rowId:
                    vec = d["vec"]
            
            if vec is None:
                return jsonify({"response": "Vector not found"}), 404

        except Exception as e:
            return jsonify({"response": str(e)}), 400

        try:
            # Find top `n` rows based on vector similarity
            query = text("""
            SELECT * 
            FROM :tableName 
            ORDER BY VECTOR_DOT_PRODUCT(vec, TO_VECTOR(:vec)) DESC
            LIMIT :n
            """)
            # Execute the query with the named parameters
            result = conn.execute(query, {'tableName': tableName, 'vec': vec, "n": n}).fetchall()
            rows = [dict(row) for row in result]
        except Exception as e:
            return jsonify({"response": str(e)}), 400

    return jsonify({"results": rows}), 200

@app.route('/insert', methods=['POST'])
def insert():
    tableName = request.json.get('tableName')
    data = linkedin_util.request_info(request.json.get('data'))  # Assuming this returns a dictionary with data
    vec = embed(";".join(data.values())).tolist()
    data["vec"] = str(vec)

    # Extract columns from data
    columns = ", ".join(data.keys())  # Example: 'About, Skills, Experiences, Interests, Education'
    
    # Create placeholders for each column (SQLAlchemy uses :key for named parameters)
    placeholders = ", ".join([f":{col}" for col in data.keys()])  # Example: ':About, :Skills, ...'
    
    # Create the SQL query
    query = f"INSERT INTO {tableName} ({columns}) VALUES ({placeholders})"
    

    with engine.connect() as conn:
        try:
            trans = conn.begin()  # Start a transaction
            # Insert the data
            conn.execute(text(query), data)
            trans.commit()  # Commit the transaction
        except Exception as inst:
            return jsonify({"response": str(inst)}), 400

    return jsonify({"response": "Data inserted successfully"}), 200

@app.route('/returnGraph', methods=['GET'])
def returnGraph():
    tableName = request.json.get('tableName')

    data = get(tableName)
    print(data)


def get(tableName):
    with engine.connect() as conn:
        try:
            # Execute the query to fetch all data from the table
            result = conn.execute(text(f"SELECT * FROM {tableName}"))
            # Get column names from the result
            columns = result.keys()

            # Convert rows into a list of dictionaries, zipping column names with each row's values
            data = [dict(zip(columns, row)) for row in result]
            return data
        except Exception as inst:
            return jsonify({"response": str(inst)}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)
