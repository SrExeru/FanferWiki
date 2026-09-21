from fastapi import Form, UploadFile, File
from pydantic import BaseModel, ConfigDict
from typing import Optional, Self

class CommunityData(BaseModel):
    id: int
    slug: str
    display_name: str
    
    icon_url: Optional[str]
    
    description: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)
    
class CommunityCreate(BaseModel):
    slug: str
    display_name: str
    description: Optional[str]
    
    icon: Optional[UploadFile] = File(None)
        
    @classmethod
    def as_form (cls, slug: str = Form(...), display_name: str = Form(...), description: Optional[str] = Form(...), icon: Optional[UploadFile] = File(None)) -> Self:
        return cls(
            slug=slug,
            display_name=display_name,
            description=description,
            icon=icon
        )
    
class CommunityEdit(BaseModel):
    display_name: str
    description: Optional[str]
    
    icon: Optional[UploadFile] = File(None)
    
    @classmethod
    def as_form (cls, display_name: str = Form(...), description: Optional[str] = Form(...), icon: Optional[UploadFile] = File(None)) -> Self:
        return cls(
            display_name=display_name,
            description=description,
            icon=icon
        )