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

@server.route('/login', methods=['POST'])
def login(request):
    auth = request.authorization
    auth = {
        'username': 'admin',
        'email': 'arpitkumar3203@gmail.com',
        'password': 'admin'
    }
    if not auth:
        return 'Authorization failed!! Missing credentials', 401
    
    # checking username and password
    email = auth.get('email')
    username = auth.get('username')
    password = auth.get('password')

    try:
        cur = mysql.connection.cursor()
        result = cur.execute(
            'select username, password from user where username=%s', (username,)
        )
        if result > 0:
            user_row = cur.fetchone()
            query_email = user_row[0]
            query_username = user_row[0]
            query_password = user_row[0]

            if query_email != email or query_username != username or query_password != password:
                return "Credential does not match!! Either Username or Password is incorrect", 401
            else:
                return createJWTToken(username, email, os.environ.get('JWT_SECRET'), True)
        else:
            return "Invalid Credential!!", 401
    except Exception as e:
        print("exception >> {}".format(e))

def createJWTToken(username: str, email: str, jwt_secret_key: str, is_admin: bool):
    return jwt.encode(
        {
            'username': username,
            'email': email,
            'expiry': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(1),
            'iat': datetime.datetime.utcnow(),
            'is_admin': is_admin
        },
        jwt_secret_key,
        algorithm="HS256"
    )


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000, debug=True)