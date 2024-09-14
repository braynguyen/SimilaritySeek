from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from sqlalchemy import create_engine, text

app = Flask(__name__)
CORS(app)

@app.route('/')
def homepage():
    return render_template('index.html') 


import iris
import json

username = 'demo'
password = 'demo'
hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
port = '1972' 
namespace = 'USER'
CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"

engine = create_engine(CONNECTION_STRING)

# CRUD operations
# table name must always be in A.B format. Otherwise SQLUser will get prefixed by default when the table is created 
# example tablename = project.tableName
# example schema = (myvarchar VARCHAR(255), myint INTEGER, myfloat FLOAT)
@app.route('/create', methods=['POST'])
def create():
    tableName = request.json.get('tableName')
    schema = request.json.get('schema')
    # print("trying connection string: ", connection_string, flush=True) # useful for debugging
    conn = engine.connect(connection_string, username, password)
    cursor = conn.cursor()
    try:
        cursor.execute(f"DROP TABLE {tableName}")
    except Exception as inst:
        # Ignore the error thrown when no table exists
        pass
    try:
        cursor.execute(f"CREATE TABLE {tableName} {schema}")
    except Exception as inst:
        return jsonify({"response": str(inst)})
    cursor.close()
    conn.commit()
    conn.close()
    return jsonify({"response": "table created"})

@app.route('/getall', methods=['POST'])
def getall():
    tableName = request.json.get('tableName')
    conn = engine.connect(connection_string, username, password)
    cursor = conn.cursor()
    try:
        cursor.execute(f"Select * From {tableName}")
        data = cursor.fetchall()
    except Exception as inst:
        return jsonify({"response": str(inst)})
    cursor.close()
    conn.commit()
    conn.close()
    print(data)
    return jsonify({"response": data})


# Example usage:
# query = "Insert into Sample.Person (name, phone) values (?, ?)"
# params = [('ABC', '123-456-7890'), ('DEF', '234-567-8901'), ('GHI', '345-678-9012')]
# cursor.executemany(query, params) // batch update
@app.route('/insert', methods=['POST'])
def insert():
    tableName = request.json.get('tableName')
    columns = request.json.get('columns')
    data = request.json.get('data')
    json_compatible_string = data.replace("(", "[").replace(")", "]").replace("'", '"')
    data = json.loads(json_compatible_string)
    qMarks = "("
    for i in range(len(data[0])):
        if i == len(data[0])-1:
            qMarks = qMarks+"?)"
            break
        qMarks = qMarks+"?,"
    query = f"INSERT INTO {tableName} {columns} VALUES {qMarks}"
    conn = engine.connect(connection_string, username, password)
    cursor = conn.cursor()
    try:
        cursor.executemany(query, data)
    except Exception as inst:
        return jsonify({"response": str(inst)}) 
    cursor.close()
    conn.commit()
    conn.close()
    return jsonify({"response": "new information added"})



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5010)


