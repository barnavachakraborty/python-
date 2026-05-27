import threading 
import time

start = time.perf_counter()

def do_something():
    print("sleeping for 5 secs")
    time.sleep(5)
    print("done Sleeping")

t1 = threading.Thread(target = do_something)
t2 = threading.Thread(target = do_something)

t1.start()
t2.start()
t1.join()
t2.join()

end = time.perf_counter()

print(f"compleated in {round(end-start,2)} second(s)")