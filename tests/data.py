from dataclasses import dataclass


@dataclass
class TokenData:
    access_token: str
    refresh_token: str
    token_type: str
    expires: int


@dataclass
class SessionData:
    session_id: str
    issued_at: int
    expires_at: int
    is_current: bool
