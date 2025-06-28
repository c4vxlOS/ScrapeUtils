import scrapeUtils as su
import argparse
import subprocess
import sys

parser = argparse.ArgumentParser(description="Allows you to easily download media.")

parser.add_argument("--out", "-o", type=str, help="The output directory where downloaded media will be saved. (Default='./download')")
parser.add_argument("--urls", "-uf", type=str, help="Specify a file of urls to download.")
parser.add_argument("--url", "-u", action="append", type=str, help="Specify a single url to download")
parser.add_argument("--timeout", "-t", type=int, help="Specify the timeout between multiple downloads [ms]")

args = parser.parse_args()

out = args.out
if not out:
    out = "."

def default(a, b): return a if a else b
urls = default(args.url, [])
if args.urls:
    urls = su.read_urls(args.urls)
elif len(urls) == 0:
    urls = [line.strip() for line in sys.stdin if line.strip()]

timeout = default(args.timeout, 0)

su.download_bulk(urls, out, timeout)

subprocess.call(["nautilus", out])