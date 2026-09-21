from fastapi import APIRouter, Depends, HTTPException
from services.database import session_manager, DBSession
from schemas.communities import CommunityCreate, CommunityData, CommunityEdit
import cloudinary.uploader
from models import Community

community_router = APIRouter(
    prefix='/community',
    tags=['Communities']
)

# User tools

@community_router.get('/search', response_model=list[CommunityData])
async def search_community(query: str, db: DBSession = Depends(session_manager.get_session)):
    communities = await db.select(Community).where(Community.display_name.ilike(f'%{query}%')).all()
    
    result = []
    
    for community in communities:
        result.append(
            CommunityData.model_validate(community)
        )
    
    return communities

# Community feed

@community_router.get('/popular')
async def popular_communities (db: DBSession = Depends(session_manager.get_session)):
    communities = await db.select(Community).all()
    
    # pending
    
    return communities  

# Community CRUD

@community_router.post('/', response_model=CommunityData)
async def create_community (create_request: CommunityCreate = Depends(CommunityCreate.as_form), db: DBSession = Depends(session_manager.get_session)):
    new_community = Community(
        slug = create_request.slug,
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
    
    return new_community

@community_router.get('/{community_slug}', response_model=CommunityData)
async def get_community (community_slug: str, db: DBSession = Depends(session_manager.get_session)):
    community = await db.select(Community).where(Community.slug == community_slug).scalar_one_or_none()
        
    if not community:
        raise HTTPException(
            status_code=404,
            detail='Community not found.'
        )
    
    return community

@community_router.put('/{community_slug}', response_model=CommunityData)
async def edit_community (community_slug: str, edit_request: CommunityEdit = Depends(CommunityEdit.as_form), db: DBSession = Depends(session_manager.get_session)):
    community = await db.select(Community).where(Community.slug == community_slug).scalar_one_or_none()
    
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
    
    return community

@community_router.delete('/{community_slug}')
async def delete_community (community_slug: str, db: DBSession = Depends(session_manager.get_session)):
    community = await db.select(Community).where(Community.slug == community_slug).scalar_one_or_none()
        
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