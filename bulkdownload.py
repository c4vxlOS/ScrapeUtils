import scrapeUtils as su
import argparse
import subprocess
import sys

parser = argparse.ArgumentParser(description="Allows you to easily download media.")

parser.add_argument("--out", "-o", type=str, help="The output directory where downloaded media will be saved. (Default='./download')")
parser.add_argument("--urls", "-uf", type=str, help="Specify a file of urls to download.")
parser.add_argument("--url", "-u", type=str, help="Specify a single url to download")

args = parser.parse_args()

out = args.out
if not out:
    out = "."

urls = []
if args.url:
    urls = [ args.url ]
elif args.urls:
    urls = su.read_urls(args.urls)
else:
    urls = [line.strip() for line in sys.stdin if line.strip()]


urls = [ u.split("] ")[1:][0] if u.startswith("[") else u for u in urls ]

su.download_bulk(urls, out)

subprocess.call(["nautilus", "."])