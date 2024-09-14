import os
import json
from sqlalchemy import create_engine, text

username = 'demo'
password = 'demo'
hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
port = '1972'
namespace = 'USER'
CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"

engine = create_engine(CONNECTION_STRING)

tableName = "MIT.People"
columns = "(About, Skills, Experiences, Interests, Education)"
data = {
        "About": "CS @ University of Pittsburgh | GHC24 Hi, I'm Rachel! I'm an undergraduate computer science student currently based in Pittsburgh. My career interests include software engineering, machine learning and AI, and game development.",
        "Skills": "Software Development Object-Oriented Programming Assembly Language CLI Java Microsoft Office Computer Science", 
        "Experiences": "Software Engineer Intern at PNC IT Intern at United States Steel Corporation Undergraduate Research Assistant at the University of Pittsburgh",
        "Interests": "",
        "Education": "University of Pittsburgh"
}
query = "(:About, :Skills, :Experiences, :Interests, :Education)"
# Convert the stringified list of tuples into an actual list of tuples
# json_compatible_string = data.replace("(", "[").replace(")", "]").replace("'", '"')
# data_list = json.loads(json_compatible_string)

# Create placeholders for the query
# num_placeholders = len(data_list[0])
# qMarks = "(" + ", ".join("?" for _ in range(num_placeholders)) + ")"
query = f"INSERT INTO {tableName} {columns} VALUES {query}"

with engine.connect() as conn:
    try:
        # Insert the data using a batch insert
        conn.execute(text(query), data)
    except Exception as e:
        print(e)
