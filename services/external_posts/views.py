from fastapi import APIRouter
from services.external_posts.schemas import ExternalPostRead
from . import client

router = APIRouter(tags=["EXTERNAL POSTS"], prefix="/external-posts")


@router.get("/{post_id}", response_model=ExternalPostRead)
async def get_post(post_id: int) -> ExternalPostRead:
    return await client.get_post(post_id=post_id)
