import asyncio
import random
import time

import httpx
from fastapi import FastAPI

app = FastAPI()


@app.post("/parse_url/")
# async parse_url
async def parse_url(url: str) -> str:
    """Asynchronous function to parse url"""
    try:
        with httpx.AsyncClient() as client:
            r = await client.get(url)
            r.raise_for_status()

            parse_time = 0.1 * random.randint(5, 10) if random.random() < 0.1 else 0.1
            await asyncio.sleep(parse_time)

            return f"Parsed {url}"
    except httpx.HTTPStatusError as e:
        return f"Error fetching {url}: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        return f"Error fetching {url}: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


# async run_test
async def run_test(n_requests: int) -> float:
    """ Asynchronous function to run test"""
    url = "https://httpbin.org/"

    async with httpx.AsyncClient() as client:
        ts = time.time()
        tasks = [client.post("http://localhost:8000/parse_url/",
                             json={"url": url}) for _ in range(n_requests)]
        await asyncio.gather(*tasks)
        return time.time() - ts

if __name__ == "__main__":
    print('Running test')
    t = asyncio.run(run_test(n_requests=100))
    print(f"Time taken: {t} seconds")
