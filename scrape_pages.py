from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import time

def scrape_text(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.contents, 'html.parser')

        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()

        text = soup.get_text(separator=" ")
        return " " .join
    except Exception as e:
        return ""
    
def scrape_all():
    df = pd.read_csv("./data/chrome_history.csv")
    output_path = "./data/scraped_pages.jsonl"

    with open(output_path, "w") as f:
        for _, row in df.iterrows():
            content = scrape_text(row['url'])
            doc = {
                "url": row['url'],
                "title": row['title'],
                "timestamp": row['last_visit_time'],
                "content": content
            }
            f.write(json.dumps(doc) + "\n")
            time.sleep(0.5)

        print(f"Scraped pages saved to {output_path}")

if __name__ == "__main__":
    scrape_all()
