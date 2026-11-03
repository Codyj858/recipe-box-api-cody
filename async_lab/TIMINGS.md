Synchronous baseline (slow-service on localhost:5001)

1 call  (/nutrition/eggs):            1.047798375 s
3 calls (/eggs, /bread, /milk):       3.07390975 s
5 calls (/eggs, /bread, /milk, ...):  5.099256333 s

“Async HTTP, sequential awaits (3 requests): 3.074s”
“Async HTTP, concurrent with asyncio.gather (3 requests): 1.057s”