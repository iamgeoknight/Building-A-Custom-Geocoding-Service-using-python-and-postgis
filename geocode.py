from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Set up the connection parameters
host = 'localhost'
port = "5432"
database = 'postgres'
user = 'postgres'
password = 'admin'


# Connect to the database
conn = psycopg2.connect(host=host, database=database, user=user, password=password, port = port)

# Open a cursor to perform database operations
cur = conn.cursor()

# Endpoint for autocomplete functionality
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    table_name = 'sample_pois'

    # Get the search term from the request
    search_term = request.args.get('search_term', '')

    # Execute a query to get the top 10 matching entries
    cur.execute(F"SELECT identifier, st_x(geometry) lon, st_y(geometry) lat FROM {table_name} where identifier ILIKE '%{search_term}%' LIMIT 10")

    # Fetch the results
    rows = cur.fetchall()
    

    # Convert the results to a JSON response
    results = []
    for row in rows:
        result = {'value': row[0], 'lon': row[1], 'lat': row[2]}  # replace 'id' and 'value' with your column names
        results.append(result)
    response = {'results': results}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)



