import asyncio
import time

async def inner():
    print("inner start")
    time.sleep(1)
    print("inner end")
    return "done"

async def worker(name, delay):
    print(name, "start")
    await asyncio.sleep(delay)
    print(name, "end")

async def outer():
    print("outer start")
    await worker("A", 1)
    inner_task = asyncio.create_task(inner())
    await worker("B", 1)
    await inner_task
    return "outer result"

result = asyncio.run(outer())
print("final:", result)
