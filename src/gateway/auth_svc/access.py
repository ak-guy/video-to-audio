import os
import requests

def login(request):
    '''
    return value -> (token, error)
    '''
    auth = request.authorization
    print(auth, flush=True)
    if not auth:
        return None, ("Credential not found", 401)
    
    auth = (auth.username, auth.password)
    print(auth, flush=True)
    # will ping to auth service to get jwt token
    conn = requests.post(
        f'http://{os.environ.get("AUTH_SERVICE_ADDRESS")}/login', auth=auth
    )

    if conn.status_code == 200:
        return conn.text, None
    print(conn.text, flush=True)
    print(conn.status_code, flush=True)
    return None, (conn.text, conn.status_code)