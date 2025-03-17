from fastapi import FastAPI, Request, Depends, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import os
import google_auth_oauthlib.flow
import logging

logger = logging.getLogger(__name__)

CLIENT_SECRETS_FILE_PATH = 'client_secrets.template.json'
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.scope["scheme"] = "https"
        response = await call_next(request)
        return response

app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)


def _get_flow() -> google_auth_oauthlib.flow.Flow:
    return google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file=CLIENT_SECRETS_FILE_PATH,
        scopes=SCOPES
    )


def verify_token(request: Request):
    flow = _get_flow()
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(403, "Invalid token")
    token = auth_header.split(' ')[1]
    return id_token.verify_oauth2_token(token, google_requests.Request(), flow.client_config.get("client_id"))


@app.get("/public_endpoint")
def get_all_moves():
    return {"user_data": "", "message": "you called an endpoint that does not require login"}


@app.get("/private_endpoint")
def get_all_moves(user_data: dict = Depends(verify_token)):
    return {"user_data": user_data, "message": "you called an endpoint that requires login"}


@app.get("/login")
def login_with_google(request: Request):
    flow = _get_flow()
    flow.redirect_uri = str(request.url_for("callback"))
    print("Redirect URI for google " + str(request.url_for("callback")))
    logger.info("redirect URI for google constent screen: " + flow.redirect_uri)
    authorization_url, _ = flow.authorization_url()
    return {"login_uri": authorization_url}


@app.get("/callback", name="callback")
def auth_callback(request: Request):
    flow = _get_flow()
    flow.redirect_uri = str(request.url_for("callback"))
    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)
    return {"id_token": flow.credentials._id_token}
