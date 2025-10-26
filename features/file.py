import hashlib
import aiohttp

async def download_and_hash(file_path: str, token: str):
    url = f'https://api.telegram.org/file/bot{token}/{file_path}'
    h = hashlib.sha256()
    total = 0
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            async for chunk in resp.content.iter_chunked(8192):
                h.update(chunk)
                total += len(chunk)
    return h.hexdigest(), total
