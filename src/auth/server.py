import jwt
import datetime
import os
# import dotenv

from flask import Flask, request
from flask_mysqldb import MySQL

# loading environment variables from .env file, but will create these env variable while starting image of the app
# dotenv.load_dotenv()

server = Flask(__name__)

# mysql config
server.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
server.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
server.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
server.config['MYSQL_PORT'] = os.environ.get('MYSQL_PORT')
server.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

mysql = MySQL(server)

@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth:
        return 'Authorization failed!! Missing credentials', 401
    
    # checking username and password
    print(f"auth service login request >> {request}", flush=True)
    username = auth.username
    password = auth.password
    print("auth login", flush=True)
    print(f"auth.username >> {username}", flush=True)
    print(type(username), flush=True)
    print(f"auth.password >> {password}", flush=True)
    print(type(password), flush=True)
    try:
        try:
            try:
                cur = mysql.connection.cursor()
            except Exception as e:
                print(f'Not able to establish connection with database >> {e}', flush=True)
                return f"Not able to establish connection with data base >> {e}", 401
            try:
                result = cur.execute(
                    "SELECT username, password FROM user WHERE username=%s", (auth.username,)
                )
            except Exception as e:
                result = 0
                print(f'Not able to query from table user in database {os.environ.get("MYSQL_DB", "Database name could not be found in environment")}, getting exception >> {e}', flush=True)
        except Exception as e:
            return f"Not able to establish connection with data base >> {e} and auth >> {auth}", 401
        if result > 0:
            user_row = cur.fetchone()
            query_email = user_row[0]
            query_username = user_row[1]
            query_password = user_row[2]

            if query_username != auth.username or query_password != auth.password:
                return "Credential does not match!! Either Username or Password is incorrect", 401
            else:
                return createJWTToken(auth.username, os.environ.get('JWT_SECRET'), True)
        else:
            return "Invalid Credential!!", 401
    except Exception as e:
        print(f"exception >> {e}", flush=True)
        return f"Invalid Credential !!! Exception >> {e}", 401

@server.route('/validate', methods=['POST'])
def validate():
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
        print(f'Exception while trying to decode jwt >> {E}', flush=True)
        return 'Not Authorized', 403
    
    return decode_jwt_token, 200

def createJWTToken(username: str, jwt_secret_key: str, is_admin: bool):
    return jwt.encode(
        {
            'username': username,
            'expiry': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(1),
            'creation_time': datetime.datetime.utcnow(),
            'is_admin': is_admin
        },
        jwt_secret_key,
        algorithm="HS256"
    )


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000, debug=True)