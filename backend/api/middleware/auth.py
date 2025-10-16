from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from core.config import settings

security = HTTPBearer()

class AuthMiddleware:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY

    async def verify_token(self, credentials: HTTPAuthorizationCredentials):
        try:
            payload = jwt.decode(
                credentials.credentials,
                self.secret_key,
                algorithms=["HS256"]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def __call__(self, request: Request, call_next):
        # Skip auth for public endpoints
        if request.url.path in ["/", "/health", "/docs", "/redoc"]:
            return await call_next(request)

        # Verify token for protected endpoints
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        credentials = HTTPAuthorizationCredentials(
            scheme=authorization.split()[0],
            credentials=authorization.split()[1]
        )

        await self.verify_token(credentials)
        return await call_next(request)