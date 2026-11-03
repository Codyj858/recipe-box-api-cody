import time
import threading
import httpx

def make_request(url):
    httpx.get(url)

def main():
    urls = [
        "http://127.0.0.1:5001/nutrition/eggs",
        "http://127.0.0.1:5001/nutrition/bacon",
        "http://127.0.0.1:5001/nutrition/toast",
    ]
    start = time.perf_counter()
    threads = []

    for url in urls:
        thread = threading.Thread(target=make_request, args=(url,))
    thread.start()
    threads.append(thread)
    for t in threads:
        t.join()
    end = time.perf_counter()
    print(f"threaded total: {end - start:.3f} seconds")

if __name__ == "__main__":
    main()
