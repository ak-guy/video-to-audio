import os
import requests

def login(request):
    '''
    return value -> (token, error)
    '''
    auth = request.authorization
    if not auth:
        return None, ("Credential not found", 401)
    
    auth = (auth.username, auth.password)

    # will ping to auth service to get jwt token
    conn = requests.post(
        f'http://{os.environ.get("AUTH_SERVICE_ADDRESS")}/login', auth=auth
    )

    if conn.status_code == 200:
        return conn.txt, None
    return None, (conn.txt, conn.status_code)