import asyncio
import httpx
import time

async def fetch_with_timeout(client, url, timeout_secs):
    try:
         return await asyncio.wait_for(client.get(url), timeout=timeout_secs)
    except asyncio.TimeoutError:
        return "Timed out"


async def main():
    async with httpx.AsyncClient() as client:
        urls = [
                "http://127.0.0.1:5001/nutrition/eggs",
                "http://127.0.0.1:5001/nutrition/bacon",
                "http://127.0.0.1:5001/nutrition/toast",
            ]
        tasks = [fetch_with_timeout(client, url, timeout_secs=1.0) for url in urls]
        responses = await asyncio.gather(*tasks)
        for url, resp in zip(urls, responses):
            if resp == "Timed out":
                print(url, "TIMED OUT")
            else:
                print(url, resp.status_code)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("took:", end - start)