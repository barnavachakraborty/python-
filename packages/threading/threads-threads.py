import threading 
import time

start = time.perf_counter()

def do_something(seconds):
    print(f"sleeping for {seconds} secs")
    time.sleep(seconds)
    print(f"done Sleeping...{seconds}")

threads = []

for i in range(10):
    t = threading.Thread(target=do_something, args=[i])
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()

end = time.perf_counter()

print(f"compleated in {round(end-start,4)} second(s)")