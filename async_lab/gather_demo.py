import asyncio
import time

async def run_quest(player, seconds):
    await asyncio.sleep(seconds)
    return f"{player} finished"

async def main():
    q1 = asyncio.create_task(run_quest("Mage", 1))
    q2 = asyncio.create_task(run_quest("Rogue", 2))
    q3 = asyncio.create_task(run_quest("Warrior", 3))
    start = time.perf_counter()
    result = await asyncio.gather(q1, q2, q3)
    end = time.perf_counter()
    print("took:", end - start)
    print("result:", result)

async def sequential_main():
    start = time.perf_counter()
    r1 = await run_quest("Mage", 1)
    r2 = await run_quest("Rogue", 2)
    r3 = await run_quest("Warrior", 3)
    end = time.perf_counter()
    print("sequential took:", end - start)
    print("sequential result", [r1, r2, r3])

if __name__ == "__main__":
    asyncio.run(main())