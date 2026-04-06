import httpx
from .schemas import ExternalPostRead

BASE_URL = "https://jsonplaceholder.typicode.com"


async def get_post(post_id: int) -> ExternalPostRead:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/posts/{post_id}")
        response.raise_for_status()
        data = response.json()
        return ExternalPostRead(**data)
