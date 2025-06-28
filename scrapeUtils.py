from tqdm import tqdm
import os
import re
import requests
import time

IMG_TYPES = [ "jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp" ]
VID_TYPES = [ "mp4", "avi", "mkv", "mov", "flv", "webm", "wmv" ]
NON_SOURCE_TYPES = IMG_TYPES + VID_TYPES

def find_url(source: str, types: list[str]) -> str:
    return re.search(r"https?://[^\s]+?\.(" + "|".join(types) + ")", source).group()

def find_urls(source: str, types: list[str]) -> list[str]:
    return re.findall(r"https?://[^\s]+?\.(?:" + "|".join(types) + ")", source)

def find_video(source: str) -> str:
    return find_url(source, VID_TYPES)

def find_videos(source: str) -> str:
    return find_urls(source, VID_TYPES)

def find_image(source: str) -> str:
    return find_url(source, IMG_TYPES)

def find_images(source: str) -> str:
    return find_urls(source, IMG_TYPES)

def get_page_source(url: str, headers = { "User-Agent": "Mozilla/5.0" }) -> str:
    if any(url.endswith(r) for r in NON_SOURCE_TYPES):
        return ""

    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else ""

def read_urls(file: str = "urls.txt") -> str:
    return [ l.strip() for l in open(file).readlines() if l.strip() and l.__contains__("http")]

def download_file(url: str, path: str) -> bool:
    try:
        response = requests.get(url, headers={ "User-Agent": "Mozilla/5.0" }, stream=True)
        response.raise_for_status()
        
        with open(path, 'wb') as file, tqdm(
            desc=f"Downloading {url}",
            total=int(response.headers.get('content-length', 0)),
            unit='B',
            unit_scale=True,
            unit_divisor=1024
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                progress_bar.update(len(chunk))
        
        return True
    except requests.exceptions.RequestException:
        return False

def download_bulk(urls: list[str], out_dir: str = "download", cooldown = 0):
    os.makedirs(out_dir, exist_ok=True)
    for url in urls:
        subdirs = url.split("] ")[0].removeprefix("[").split(";") if url.__contains__("] ") else []
        subpath = "/".join(subdirs)
        dir = os.path.join(out_dir, subpath)
        os.makedirs(dir, exist_ok=True)
        url = "] ".join(url.split("] ")[1:])

        success = download_file(url, os.path.join(dir, os.path.basename(url).split("?")[0].split(":")[0].split(";")[0][:255]))

        if success:
            print(f"Successfully downloaded {url}.")
        else:
            print(f"Could not download {url}.")
        
        time.sleep(cooldown)