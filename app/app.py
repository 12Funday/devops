from flask import Flask, jsonify, request

import json
import logging
import traceback
import sqlite3
import os.path

# init app
app = Flask(__name__)


# basic logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# basic DB with sqlite3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'Bookstore.db')

# init connection
def get_db():
    try:
        db = sqlite3.connect(DATABASE)
        logger.info(f"Connected to database {DATABASE}")
        return db
    except Exception:
        tb = traceback.format_exc()
        logger.error(f'Error : {tb}')

@app.route('/', methods=['GET'])
def hello():
    data = {"Hello":"World!"}
    return jsonify(data)

@app.route('/book', methods=['GET', 'POST'])
def books():
    # handle GET request
    if request.method == 'GET':
        data = []
        sql = 'SELECT * FROM books'
        cur = get_db().cursor()
        cur.execute(sql)
        results = cur.fetchall()
        logger.info(f'hasil query : {results}')
        cur.close()
        for r in results:
            buku = {
                "id" : r[0],
                "title" : r[1],
                "author" : r[2]
            }
            data.append(buku)

        logger.info(f"List of books : {data}")
        return jsonify(data)
    # handle post request
    if request.method == 'POST':
        data = json.loads(request.get_data())
        logger.info(f'datanya : {data}')
    
        params = (
            data['title'],
            data['author']
        )
        sql = 'insert into books(title, author) values (?, ?)'
        try:
            conn = get_db()
            cur = conn.cursor()
            logger.info(f'Inserting data {params} to database')
            insert_book = cur.execute(sql, params)
            conn.commit()
            cur.close()

            status = {
                "status" : 200,
                "Message" : "Data successfully inserted"
            }
            return jsonify(status)
        
        except:
            tb = traceback.format_exc()
            logger.error(f'Error : {tb}')
            status = {"Status" : 500, "Message" : "Internal Server Error"}
            return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True)