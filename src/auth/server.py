import jwt
import os
import datetime

from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT", 3306))


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401

    try:
        # check db for username and password
        cur = mysql.connection.cursor()
        res = cur.execute(
            "SELECT email, password FROM user WHERE email=%s", (auth.username,)
        )
    except Exception as e:
        print(f'Exception >> {e}', flush=True)
        try:
            server.config["MYSQL_HOST"] = "192.168.49.2"
            cur = mysql.connection.cursor()
            res = cur.execute(
                "SELECT email, password FROM user WHERE email=%s", (auth.username,)
            )
        except Exception as e:
            print(f'Could not connect to database >> {e}', flush=True)
            return "Internal Server Error !!", 500

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET", "somedummyval"), True)
    else:
        return "invalide credentials", 401

@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    authenticationType, encoded_jwt = encoded_jwt.split(" ")
    if authenticationType != "Bearer":
        return "Must use bearer token", 403

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET", "somedummyval"), algorithms=["HS256"]
        )
    except Exception as e:
        return f"not authorized, {e}", 403

    return decoded, 200

def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "isAdmin": authz,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
