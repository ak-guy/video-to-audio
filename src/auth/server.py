import jwt
import datetime
import os
# import dotenv

from flask import Flask
from flask_mysqldb import MySQL

# loading environment variables from .env file, but will create these env variable while starting image of the app
# dotenv.load_dotenv()

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
        print(f"exception >> {e}")

@server.route('/validate', methods=['POST'])
def validate(request):
    encoded_jwt = request.headers['Authorization']

    if not encoded_jwt:
        return "Missing Credential !!", 401
    
    jwt_token = encoded_jwt.split(" ")[1]

    try:
        decode_jwt_token = jwt.decode(
            encoded_jwt,
            os.environ.get('JWT_SECRET'),
            algorithms=['HS256']
        )
    except Exception as E:
        print(f'Exception while trying to decode jwt >> {E}')
        return 'Not Authorized', 403
    
    return decode_jwt_token, 200

def createJWTToken(username: str, email: str, jwt_secret_key: str, is_admin: bool):
    return jwt.encode(
        {
            'username': username,
            'email': email,
            'expiry': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(1),
            'creation_time': datetime.datetime.utcnow(),
            'is_admin': is_admin
        },
        jwt_secret_key,
        algorithm="HS256"
    )


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000, debug=True)