from fastapi import APIRouter, Depends, HTTPException
from backend.services.database import session_manager, AsyncSession
from backend.models import Community
from sqlalchemy import select
from typing import Optional

community_router = APIRouter(
    prefix='/community',
    tags=['Communities']
)

@community_router.post('/new')
async def create_community (name: str, display_name: str, description: Optional[str], db: AsyncSession = Depends(session_manager.get_session)):
    new_community = Community(
        name = name,
        display_name = display_name,
        description = description
    )
    
    db.add(new_community)
    await db.commit()
    await db.refresh(new_community)
    
    return new_community

@community_router.get('/{community_id}')
async def get_community (community_id: int, db: AsyncSession = Depends(session_manager.get_session)):
    query = await db.execute(
            select(Community).where(Community.id == community_id)
        )
        
    community = query.scalars().first()
        
    if not community:
        raise HTTPException(
            status_code=404,
            detail='Community not found.'
        )
    
    return community

@community_router.put('/{community_id}')
async def edit_community (community_id: int, display_name: str, description: Optional[str], db: AsyncSession = Depends(session_manager.get_session)):
    query = await db.execute(
        select(Community).where(Community.id == community_id)
    )
    
    community = query.scalars().first()
    
    if not community:
        raise HTTPException(
            status_code=404,
            detail='Community not found.'
        )
    
    community.display_name = display_name
    community.description = description
    
    await db.commit()
    await db.refresh(community)
    
    return community

@community_router.delete('/{community_id}')
async def delete_community (community_id: int, db: AsyncSession = Depends(session_manager.get_session)):
    query = await db.execute(
            select(Community).where(Community.id == community_id)
        )
        
    community = query.scalars().first()
        
    if not community:
        raise HTTPException(
            status_code=404,
            detail='Community not found.'
        )
        
    await db.delete(community)
    await db.commit()
    
    return 'Community deleted.'