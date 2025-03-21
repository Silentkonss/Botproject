import psycopg2, os
from dotenv import load_dotenv

load_dotenv()

with psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
) as conn:

    def create_db():

        with conn.cursor() as cur:
            cur.execute(""" CREATE TABLE IF NOT EXISTS chatuser(
                                            chat_id BIGINT PRIMARY KEY,
                                            user_name VARCHAR(255),
                                            topic_id INTEGER);""")
            conn.commit()
        return

create_db()