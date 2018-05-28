from ebay_deal_scraper.scraper import scrape

data = scrape()
file_name = f"deals-{data['date']}"
print(data)
print(file_name)
