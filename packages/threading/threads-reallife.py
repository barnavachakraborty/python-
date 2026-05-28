import requests
import time 
import concurrent.futures as futures
import logging

logging.basicConfig(filename = "log.log", level = logging.INFO, format = "\n%(asctime)s\n%(message)s")
info = []

img_urls = [
    'https://images.unsplash.com/photo-1516117172878-fd2c41f4a759',
    'https://images.unsplash.com/photo-1532009324734-20a7a5813719',
    'https://images.unsplash.com/photo-1524429656589-6633a470097c',
    'https://images.unsplash.com/photo-1530224264768-7ff8c1789d79',
    'https://images.unsplash.com/photo-1564135624576-c5c88640f235',
    'https://images.unsplash.com/photo-1541698444083-023c97d3f4b6',
    'https://images.unsplash.com/photo-1522364723953-452d3431c267',
    'https://images.unsplash.com/photo-1513938709626-033611b8cc03',
    'https://images.unsplash.com/photo-1507143550189-fed454f93097',
    'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e',
    'https://images.unsplash.com/photo-1504198453319-5ce911bafcde',
    'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99',
    'https://images.unsplash.com/photo-1516972810927-80185027ca84',
    'https://images.unsplash.com/photo-1550439062-609e1531270e',
    'https://images.unsplash.com/photo-1549692520-acc6669e2f0c'
]
def download_img(url:str):
    img_bytes = requests.get(url).content
    img_name = url.split('/')[-1] + '.jpg'
    with open(img_name,'wb') as img:
        img.write(img_bytes)
        info.append(f"{img_name} is downloaded...\n")

t1 = time.perf_counter()
with futures.ThreadPoolExecutor() as executor:
    executor.map(download_img,img_urls)
t2 = time.perf_counter()

info.append(f"took {round(t2-t1,2)} seconds...\n")
logging.info("".join(info))
