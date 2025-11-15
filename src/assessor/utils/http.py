from httpx import AsyncClient, Response, HTTPStatusError

async def fetch(url: str) -> Response:
    async with AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response

def is_valid_response(response: Response) -> bool:
    return response.status_code == 200

def extract_json(response: Response) -> dict:
    return response.json() if is_valid_response(response) else {}

def extract_text(response: Response) -> str:
    return response.text if is_valid_response(response) else ''