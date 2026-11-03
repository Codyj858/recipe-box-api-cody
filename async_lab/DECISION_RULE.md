# Execution Model Decision Rule (DRAFT)

## 1. When to use simple synchronous code

- Use a single, synchronous flow when:
  - You only have a small number of calls.
  - Calls depend on each other (A must finish before B).
  - Current performance is acceptable.
- Reason: simplest to read, test, and debug. No threading or async complexity.

## 2. When to use threads

- Use threads when:
  - You have multiple **independent blocking I/O** calls (HTTP, DB, disk).
  - You want those I/O waits to **overlap**.
  - You must keep using **synchronous** libraries (like normal `httpx`).
- Evidence from my timings:
  - Sequential HTTP: about 3 seconds total for 3 calls.
  - Threaded HTTP: about 1 second total for the same 3 calls.
- Reason: threads can run while others are blocked on I/O, so total wall time drops.

## 3. When to consider async

- Consider async when:
  - You have **many** concurrent I/O operations.
  - You want more efficient concurrency than threads for networking.
  - Your stack supports async libraries and patterns.
- Reason: async can manage large numbers of concurrent I/O operations, but needs different code style and tools.

## 4. CPU-bound work

- Threads did **not** improve my pure Python CPU loop:
  - Sequential CPU loop: ~1.0 seconds.
  - 4 threaded CPU loops (same work per thread): ~4.0 seconds.
- Reason: under CPython’s **global interpreter lock (GIL)**, only one thread runs Python bytecode at a time, so CPU-bound threads just take turns and add overhead.
- For true CPU-bound speedups, the right answer is **multiple processes**, but that is **out of scope for this lesson**.


Use simple sync when work is small, ordered, or “fast enough.”
Use threads when you need concurrency for blocking I/O with sync libraries.
Consider async when you have lots of concurrent I/O and can adopt async-friendly tools.
For CPU-bound speedups, use processes, not threads (out of scope here).


When I have many independent I/O-bound operations (like several HTTP requests to a slow service) in one place, I should prefer async + asyncio.gather so the waits overlap and total time is closer to the slowest call, not the sum.

If the work is CPU-bound or there aren’t multiple independent waits, async won’t make it faster and may add useless complexity.

My measurements with 3 HTTP calls (≈3.07s sequential vs ≈1.06s concurrent) support using async for overlapping I/O waits, but they do not say anything about CPU performance or overall server throughput.

