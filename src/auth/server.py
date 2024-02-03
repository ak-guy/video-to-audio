import jwt
import datetime
import os
import dotenv

from flask import Flask
from flask_mysqldb import MySQL

# loading environment variables from .env file
dotenv.load_dotenv()

server = Flask(__name__)
mysql = MySQL(server)

# mysql config
server.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
server.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
server.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
server.config['MYSQL_PORT'] = os.environ.get('MYSQL_PORT')
server.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
print(server.config.get('MYSQL_DB'))

@server.route('/login', methods=['POST'])
def login(request):
    auth = request.authorization
    if not auth:
        return 'Authorization failed!! Missing credentials', 401
    
    # checking username and password
    


if __name__ == '__main__':
    server.run(debug=True)