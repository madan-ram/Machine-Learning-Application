import Crawler

def main():
	Crawl=Crawler.Crawl()
	Crawl.BFSCrawl(("http://en.wikipedia.org/wiki/Tourism_in_India","Indian Tourism"))

if __name__ == "__main__":
    main()