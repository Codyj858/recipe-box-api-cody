import asyncio
import httpx
import time

async def main():
    async with httpx.AsyncClient() as client:
        urls = [
                "http://127.0.0.1:5001/nutrition/eggs",
                "http://127.0.0.1:5001/nutrition/bacon",
                "http://127.0.0.1:5001/nutrition/toast",
            ]
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        for resp in responses:
            print(resp.url, resp.status_code)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print("took:", end - start)