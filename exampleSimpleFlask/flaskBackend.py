from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sqlalchemy import create_engine, text
import os
import json

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


# CRUD operations

# Create a table
@app.route('/create', methods=['POST'])
def create():
    tableName = request.json.get('tableName')
    schema = request.json.get('schema')

    with engine.connect() as conn:
        try:
            # Drop the table if it exists
            conn.execute(text(f"DROP TABLE {tableName}"))
        except Exception:
            pass  # Ignore error if the table doesn't exist

        try:
            # Create the table with the provided schema
            conn.execute(text(f"CREATE TABLE {tableName} {schema}"))
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
            data = [dict(row) for row in result]
        except Exception as inst:
            return jsonify({"response": str(inst)}), 400

    return jsonify({"response": data}), 200


# Insert data into a table
@app.route('/insert', methods=['POST'])
def insert():
    tableName = request.json.get('tableName')
    columns = request.json.get('columns')  # Example: "(name, phone)"
    data = request.json.get('data')  # Example: "[(val1, val2), (val3, val4)]"

    # Convert the stringified list of tuples into an actual list of lists
    json_compatible_string = data.replace("(", "[").replace(")", "]").replace("'", '"')
    data_list = json.loads(json_compatible_string)

    # Create placeholder marks for query
    qMarks = ", ".join(["?" for _ in range(len(data_list[0]))])
    query = f"INSERT INTO {tableName} {columns} VALUES ({qMarks})"

    with engine.connect() as conn:
        try:
            # Insert the data using a batch insert
            conn.execute(text(query), data_list)
        except Exception as inst:
            return jsonify({"response": str(inst)}), 400

    return jsonify({"response": "Data inserted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)
