import os, pandas as pd
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text

username = 'demo'
password = 'demo'
hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
port = '1972' 
namespace = 'USER'
CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"

engine = create_engine(CONNECTION_STRING)

with engine.connect() as conn:
    with conn.begin():# Load 
        sql = f"""
                CREATE TABLE scotch_reviews (
        name VARCHAR(255),
        category VARCHAR(255),
        review_point INT,
        price DOUBLE,
        description VARCHAR(2000),
        description_vector VECTOR(DOUBLE, 384)
        )
                """
        result = conn.execute(text(sql))