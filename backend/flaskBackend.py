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


# CRUD operations

# Create a table
@app.route('/create', methods=['POST'])
def create():
    tableName = request.json.get('tableName')
    schema = "(URL VARCHAR(255), About VARCHAR(255), Skills VARCHAR(255), Experiences VARCHAR(255), Interests VARCHAR(255), Education VARCHAR(255)), vec VECTOR(DOUBLE, 384)"

    with engine.connect() as conn:
        try:
            trans = conn.begin()  # Start a transaction
            # Drop the table if it exists
            conn.execute(text(f"DROP TABLE {tableName}"))
            trans.commit()  # Commit the transaction

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
            # Get column names from the result
            columns = result.keys()

            # Convert rows into a list of dictionaries, zipping column names with each row's values
            data = [dict(zip(columns, row)) for row in result]
            print(data)
        except Exception as inst:
            return jsonify({"response": str(inst)}), 400

    return jsonify({"response": data}), 200


@app.route('/insert', methods=['POST'])
def insert():
    tableName = request.json.get('tableName')
    data = linkedin_util.request_dummy_info()  # Assuming this returns a dictionary with data
    vector = embed(";".join(data.values()))
    data["vec"] = vector

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



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)
