Synchronous baseline (slow-service on localhost:5001)

1 call  (/nutrition/eggs):            1.047798375 s
3 calls (/eggs, /bread, /milk):       3.07390975 s
5 calls (/eggs, /bread, /milk, ...):  5.099256333 s

“Async HTTP, sequential awaits (3 requests): 3.074s”
“Async HTTP, concurrent with asyncio.gather (3 requests): 1.057s”


sequential: ~2.14s for 2 slow nutrition calls
async concurrent: ~1.05s for the same 2 calls
note that the async view stays responsive with fallback when the slow service is stopped


Async is a good fit because this endpoint makes independent, I/O-bound HTTP calls, and asyncio.gather lets those waits overlap so the total latency is close to one slow call instead of two.
I rejected a fully synchronous view because it would block on each call in sequence, doubling latency for no gain.
I also rejected threads because they add extra overhead and complexity, while async with httpx.AsyncClient already gives efficient concurrency for this kind of network-bound work.