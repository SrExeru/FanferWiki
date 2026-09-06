from pydantic import BaseModel
from typing import Optional

class CommunityData(BaseModel):
    id: int
    name: str
    display_name: str
    description: Optional[str]
    
class CommunityCreate(BaseModel):
    name: str
    display_name: str
    description: Optional[str]
    
class CommunityEdit(BaseModel):
    display_name: str
    description: Optional[str]