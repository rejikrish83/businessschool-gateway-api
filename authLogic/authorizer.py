from fastapi import Depends, FastAPI, HTTPException, status,Header
from authLogic.AuthLogic import AuthLogic
import json
# Read configuration from JSON file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Extract MongoDB connection details
OKTA_ISSUER = config["okta"]["uri"]
CLIENT_ID = config["okta"]["clientId"]
AUDIENCE = config["okta"]["audience"]

# OKTA_ISSUER = "https://{yourOktaDomain}/oauth2/default"
#CLIENT_ID = "yourClientId"
#AUDIENCE = "api://default"
async def has_access(authorization: str = Header(...)):
    authLogic = AuthLogic(authorization, OKTA_ISSUER, CLIENT_ID, AUDIENCE)
    payload =  await authLogic.verifyToken()
    return payload

