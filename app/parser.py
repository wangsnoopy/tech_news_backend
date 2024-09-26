from rss_to_json import fetch_rss_to_json, fetch_products_to_json

if __name__ == "__main__":
    rss_url = "https://news.ycombinator.com/rss"
    rss_url_products = "https://www.producthunt.com/feed"
    articles = fetch_rss_to_json(rss_url)
    products = fetch_products_to_json(rss_url_products)
    print(f"Fetched and inserted {len(articles)} news into MongoDB.")
    print(f"Fetched and inserted {len(products)} products into MongoDB.")