import multiprocessing
import time

start= time.perf_counter()

def do_something(seconds):
    print(f"Sleeping for {seconds} seconds" )
    time.sleep(seconds)
    print(f"Done Sleeping...{seconds}")

if __name__ == "__main__":
    processes = []

    for i in range(10):
        p = multiprocessing.Process(target=do_something,args=[i])
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

    finish = time.perf_counter()

    print(f"took {round(finish-start,2)}")
