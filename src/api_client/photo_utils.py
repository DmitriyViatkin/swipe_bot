import httpx


async def download_photo(url: str) -> bytes | None:
    try:
        async with httpx.AsyncClient(
            verify=False, timeout=10.0, follow_redirects=True
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content

    except Exception as e:
        print(f"Не вдалось завантажити фото: {e}")
        return None
