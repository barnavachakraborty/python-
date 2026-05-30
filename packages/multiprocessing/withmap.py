import concurrent.futures as futures
import time



def do_something(seconds:int):
    print(f"Sleeping for {seconds} seconds" )
    time.sleep(seconds)
    return f"Done Sleeping...{seconds}"


if __name__ == "__main__":
    start = time.perf_counter()
    with futures.ProcessPoolExecutor() as executor:
        secs = [1, 2, 3, 4, 5]
        results = executor.map(do_something,secs)
        for result in results:
            print(result)
    end =  time.perf_counter()

    print(f"took {round(end-start,2)} seconds")