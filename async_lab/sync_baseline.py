import time
import httpx

start = time.perf_counter()
httpx.get("http://127.0.0.1:5001/nutrition/eggs")
httpx.get("http://127.0.0.1:5001/nutrition/bread")
httpx.get("http://127.0.0.1:5001/nutrition/milk")
httpx.get("http://127.0.0.1:5001/nutrition/cheese")
httpx.get("http://127.0.0.1:5001/nutrition/apple")
end = time.perf_counter()
print("Elapsed for 5 calls:", end - start)