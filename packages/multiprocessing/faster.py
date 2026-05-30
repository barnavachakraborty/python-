import concurrent.futures as futures
import time

def do_something(seconds:int):
    print(f"Sleeping for {seconds} seconds" )
    time.sleep(seconds)
    return f"Done Sleeping...{seconds}"

if __name__ == "__main__":
    with futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(do_something,i) for i in range(1,11)]
        for f in futures.as_completed(results):
            print(f.result())