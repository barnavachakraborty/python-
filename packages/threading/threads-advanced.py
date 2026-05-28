import concurrent.futures
import time

def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return f'Done sleeping {seconds} second(s)'
start = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor() as executer:
    # secs = [1,2,3,4,5,]
    # results =[executer.submit(do_something,sec) for  sec in secs]

    # for  f in concurrent.futures.as_completed(results):
    #     print(f.result())
    """
    better way:
    """
    secs = [1,2,3,4,5,]
    results =executer.map(do_something,secs)
    for result in results:
        print(result)


end = time.perf_counter()

print(f"Compleated in {round(end -start,2)} secs")

