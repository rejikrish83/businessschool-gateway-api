from fastapi import Depends, FastAPI, HTTPException, status,Header
from jose import JWTError
from okta_jwt_verifier import JWTVerifier
class AuthLogic:

    def __init__(self, token, issuer, clientId, AUDIENCE):
        self.token = token
        self.issuer = issuer
        self.clientId = clientId
        self.aud = AUDIENCE

    def verifyToken(self):
        if not self.token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")

        token = self.token.split("Bearer ")[1]
        print(token)
        print(self.aud)
        print(self.issuer)

        try:
            # jwt_verifier = JWTVerifier(CLIENT_ID, OKTA_ISSUER)
            jwt_verifier = JWTVerifier(issuer=self.issuer, audience=self.aud)
            payload = jwt_verifier.verify_access_token(token)

            print(payload)
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
