import time
import threading

def count(n):
    total = 0
    for i in range(n):
        total += i
    return total

def run_in_threads(num_threads, n):
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=count, args=(n,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

def main():
    n = 50_000_000  # or smaller if this is too slow
    start = time.perf_counter()
    count(n)
    end = time.perf_counter()
    print(f"sequential CPU total: {end - start:.3f} seconds")
    
    num_threads = 4
    start = time.perf_counter()
    run_in_threads(num_threads, n)
    end = time.perf_counter()
    print(f"threaded CPU total: {end - start:.3f} seconds")

if __name__ == "__main__":
    main()