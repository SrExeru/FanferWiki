from fastapi import APIRouter, Depends, HTTPException
from services.database import session_manager, AsyncSession
from schemas import community_schemas
from sqlalchemy import select
from models import Community

community_router = APIRouter(
    prefix='/community',
    tags=['Communities']
)

@community_router.post('/', response_model=community_schemas.CommunityData)
async def create_community (create_request: community_schemas.CommunityCreate, db: AsyncSession = Depends(session_manager.get_session)):
    new_community = Community(
        name = create_request.name,
        display_name = create_request.display_name,
        description = create_request.description
    )
    
    db.add(new_community)
    await db.commit()
    await db.refresh(new_community)
    
    return new_community

@community_router.get('/{community_id}', response_model=community_schemas.CommunityData)
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

@community_router.put('/{community_id}', response_model=community_schemas.CommunityData)
async def edit_community (community_id: int, edit_request: community_schemas.CommunityEdit, db: AsyncSession = Depends(session_manager.get_session)):
    query = await db.execute(
        select(Community).where(Community.id == community_id)
    )
    
    community = query.scalars().first()
    
    if not community:
        raise HTTPException(
            status_code=404,
            detail='Community not found.'
        )
    
    community.display_name = edit_request.display_name
    community.description = edit_request.description
    
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