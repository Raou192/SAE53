from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt
import requests

from app.core.config import settings

bearer_scheme = HTTPBearer()

_JWKS = None


def fetch_jwks():
    base = settings.KEYCLOAK_INTERNAL_ISSUER or settings.KEYCLOAK_ISSUER
    jwks_url = f"{base}/protocol/openid-connect/certs"
    try:
        resp = requests.get(jwks_url, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Impossible de contacter Keycloak (JWKS) : {exc}",
        )
    return resp.json()


def get_jwks():
    global _JWKS
    if _JWKS is None:
        _JWKS = fetch_jwks()
    return _JWKS


def decode_token(token: str):
    jwks = get_jwks()

    try:
        header = jwt.get_unverified_header(token)
        kid = header["kid"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header de token invalide",
        )

    key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
    if key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé de signature introuvable dans le JWKS",
        )

    try:
        print(token)
        print(key)
        print(settings.KEYCLOAK_AUDIENCE)
        print(settings.KEYCLOAK_ISSUER)
        return jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.KEYCLOAK_AUDIENCE,
            issuer=settings.KEYCLOAK_ISSUER,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
        )


async def get_current_user(token=Depends(bearer_scheme)):
    payload = decode_token(token.credentials)
    return payload
