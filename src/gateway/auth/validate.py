import os
import requests

def token(request):
    if not "Authorization" in request.headers:
        return None, ("Missing Credentials", 401)
    
    token = request.headers['Authorization']

    if not token:
        return None, ("Missing Credentials", 401)
    
    conn = requests.post(
        f'http://{os.environ.get("AUTH_SERVICE_ADDRESS")}/validate',
        headers={"Authorization": token}
    )

    if conn.status_code == 200:
        return conn.txt, None

    return None, (conn.txt, conn.status_code) 