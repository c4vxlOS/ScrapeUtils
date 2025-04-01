import scrapeUtils as su
import sys
import requests
import argparse
import base64

def read_path(path: str):
    if path.startswith("http://") or path.startswith("https://"):
        response = requests.get(path, headers={ "User-Agent": "Mozilla/5.0" })
        return response.content if response.status_code == 200 else None
    else:
        with open(path, "rb") as file:
            return file.read()

def convert(path):
    return base64.b64encode(read_path(path)).decode("utf-8")

parser = argparse.ArgumentParser(description="Allows you to easily scrape media.")

parser.add_argument("--urls", "-uf", type=str, help="Specify a file of URLs to convert.")
parser.add_argument("--url", "-u", type=str, help="Specify a single URL to convert.")
parser.add_argument("--dump", "-d", type=str, help="Dump all converted links into a file.")

args = parser.parse_args()

urls = []
if args.url:
    urls = [ args.url ]
elif args.urls:
    urls = su.read_urls(args.urls)
else:
    urls = [line.strip() for line in sys.stdin if line.strip()]

converted = []
for url in urls:
    type = url.split(".").pop()
    if type in su.VID_TYPES:
        prefix = f"data:video/{type};base64, "
    elif type in su.IMG_TYPES:
        prefix = f"data:image/{type};base64, "
    else:
        prefix = f"data:unknown/{type};base64, "
    
    converted.append(f"{prefix}{convert(url)}")

for c in converted:
    print(c)

if args.dump:
    with open(args.dump, "w") as file:
        file.write("\n".join(converted))