import os
import scrapeUtils as su
import sys
import argparse
import concurrent.futures

def parse_arguments():
    parser = argparse.ArgumentParser(description="Allows you to easily scrape media.")
    parser.add_argument("--video", "-v", action="store_true", help="Download the first 'n' videos found on each site.")
    parser.add_argument("--videos", "-vs", action="store_true", help="Download all videos found on each site.")
    parser.add_argument("--image", "-i", action="store_true", help="Download the first 'n' images found on each site.")
    parser.add_argument("--images", "-is", action="store_true", help="Download all images found on each site.")
    parser.add_argument("--n", "-num", type=int, default=1, help="Set the amount of items to be scraped.")
    parser.add_argument("--urls", "-uf", type=str, help="Specify a file of URLs to scrape.")
    parser.add_argument("--url", "-u", type=str, help="Specify a single URL to scrape.")
    parser.add_argument("--dumplinks", "-dl", type=str, help="Dump all found media links into a file.")
    return parser.parse_args()

def load_urls(args):
    if args.url:
        return [args.url]
    elif args.urls:
        return su.read_urls(args.urls)
    else:
        return [line.strip() for line in sys.stdin if line.strip()]

def find_videos(url):
    source = su.get_page_source(url)
    if not source:
        print(f"Skipping {url}")
        return [ url ]
    r = su.find_videos(source)
    print(f"Found {len(r)} videos on {url}")
    return r

def find_images(url):
    source = su.get_page_source(url)
    if not source:
        print(f"Skipping {url}")
        return [ url ]
    r = su.find_images(source)
    print(f"Found {len(r)} images on {url}")
    return r

def scrape_urls(urls, scrape_function, limit=None):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(scrape_function, url): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            try:
                data = future.result()
                if limit:
                    results.extend(data[:limit])
                else:
                    results.extend(data)
            except Exception as e:
                print(f"Error scraping {futures[future]}: {e}")
    return results

def main():
    args = parse_arguments()
    urls = load_urls(args)
    out = []
    if args.video:
        out.extend(scrape_urls(urls, find_videos, args.n))
    elif args.videos:
        out.extend(scrape_urls(urls, find_videos))
    elif args.image:
        out.extend(scrape_urls(urls, find_images, args.n))
    elif args.images:
        out.extend(scrape_urls(urls, find_images))

    os.system("cls" if os.name == "nt" else "clear")
    for u in out:
        print(u)

    if args.dumplinks:
        with open(args.dumplinks, "w") as f:
            f.write("\n".join(out))

if __name__ == "__main__":
    main()