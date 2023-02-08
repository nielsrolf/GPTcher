from typing import Dict, List, Optional, Union
from pydantic import BaseModel


class Message(BaseModel):
    text: str
    user_id: Optional[str] = None
    sender: Optional[str] = None
    text_en: Optional[str] = None
    text_translated: Optional[str] = None
    voice_url: Optional[str] = None
    session: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    id: Optional[Union[str, int]] = None
    evaluation: Optional[Dict] = None