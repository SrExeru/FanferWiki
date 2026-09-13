from fastapi import APIRouter, Depends, HTTPException
from services.database import session_manager, DBSession
from schemas import community_schemas
from sqlalchemy import select
import cloudinary.uploader
from models import Community

community_router = APIRouter(
    prefix='/community',
    tags=['Communities']
)

# Community feed

@community_router.get('/popular')
async def popular_communities (db: DBSession = Depends(session_manager.get_session)):
    communities = await db.select(Community).all()

    for community in communities:
        print(community)
    
    print("-", communities)
    
    return communities  

# Community CRUD

@community_router.post('/', response_model=community_schemas.CommunityData)
async def create_community (create_request: community_schemas.CommunityCreate = Depends(community_schemas.CommunityCreate.as_form), db: DBSession = Depends(session_manager.get_session)):
    new_community = Community(
        name = create_request.name,
        display_name = create_request.display_name,
        description = create_request.description
    )
    
    if create_request.icon:
        icon = cloudinary.uploader.upload(
            create_request.icon.file,
            folder='icons'
        )
    
    icon_url = icon.get('secure_url')
    icon_id = icon.get('public_id')
    
    new_community.icon_url = icon_url
    new_community.icon_id = icon_id
    
    db.add(new_community)
    await db.commit()
    await db.refresh(new_community)
    
    return new_community

@community_router.get('/{community_id}', response_model=community_schemas.CommunityData)
async def get_community (community_id: int, db: DBSession = Depends(session_manager.get_session)):
    community = await db.select(Community).where(Community.id == community_id).scalar_one_or_none()
        
    if not community:
        raise HTTPException(
            status_code=404,
            detail='Community not found.'
        )
    
    return community

@community_router.put('/{community_id}', response_model=community_schemas.CommunityData)
async def edit_community (community_id: int, edit_request: community_schemas.CommunityEdit = Depends(community_schemas.CommunityEdit.as_form), db: DBSession = Depends(session_manager.get_session)):
    community = await db.select(Community).where(Community.id == community_id).scalar_one_or_none()
    
    if not community:
        raise HTTPException(
            status_code=404,
            detail='Community not found.'
        )
    
    community.display_name = edit_request.display_name
    community.description = edit_request.description
    
    if edit_request.icon:
        if community.icon_id:
            cloudinary.uploader.upload(
                edit_request.icon.file,
                public_id=community.icon_id,
                overwrite=True,
                invalidate=True
            )
        else:
            cloudinary.uploader.upload(
                edit_request.icon.file,
                folder='icons'
            )
    
    await db.commit()
    await db.refresh(community)
    
    return community

@community_router.delete('/{community_id}')
async def delete_community (community_id: int, db: DBSession = Depends(session_manager.get_session)):
    community = await db.select(Community).where(Community.id == community_id).scalar_one_or_none()
        
    if not community:
        raise HTTPException(
            status_code=404,
            detail='Community not found.'
        )
    
    if community.icon_id:
        cloudinary.uploader.destroy(community.icon_id)
        
    await db.delete(community)
    await db.commit()
    
    return 'Community deleted.'