import datetime as dt
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError

from gptcher import bot
from gptcher_api.schema import Message


load_dotenv(override=True)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


class TokenPayload(BaseModel):
    sub: str
    exp: int


async def get_current_user(token: str = Depends(reuseable_oauth)) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM], audience="authenticated")
        token_data = TokenPayload(**payload)
        
        new_messages = []
        async def reply_func(text):
            if not text.startswith("Corrected:"):
                new_messages.append(Message(text=text, sender='Teacher'))

        user = bot.User(token_data.sub , reply_func=reply_func)
        user.new_messages = new_messages

        if dt.datetime.fromtimestamp(token_data.exp) < dt.datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
