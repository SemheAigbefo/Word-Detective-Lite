import secrets
from fastapi import Cookie, Response

COOKIE_NAME = 'session_id'

def ensure_session(response: Response, session_id: str | None) -> str:
    if not session_id:
        session_id = secrets.token_hex(16)
        response.set_cookie(
            key=COOKIE_NAME,
            value=session_id,
            httponly=True,
            samesite='lax',
            path='/'
        )
    return session_id
