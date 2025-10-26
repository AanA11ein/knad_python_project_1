import asyncio
import aiohttp

async def do_get(url: str, retries: int = 1) -> dict | str:
    http_session = aiohttp.ClientSession()
    data = None
    error = None
    for attempt in range(1, retries + 1):
        try:
            async with http_session.get(url, timeout=10) as res:
                if res.status == 200:
                    data = await res.json()
                    break
                else:
                    error = Exception()
        except Exception as e:
            print(e)
            error = e
        await asyncio.sleep(1 * attempt)
    if http_session:
        await http_session.close()

    if error:
        raise error

    return data