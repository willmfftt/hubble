from page_scraper import PageScraper

scraper = PageScraper("https://www.deepweb-sites.com/top-50-dark-web-onion-domains-pagerank/")
links = scraper.get_all_onion_links()

for link in links:
    print link