import requests
import json
from datetime import datetime

# Put your API key here
API_KEY = '7edfaeb8bab2435dabeeadc468506996'  

# Configuration
QUERY = 'Egypt'
LANGUAGE = 'en'
PAGE_SIZE = 100
TODAY = datetime.now().strftime('%Y-%m-%d')
FILENAME = f'data/egypt_news_{TODAY}.json'

# Build the request URL
url = (
    f'https://newsapi.org/v2/everything?'
    f'q={QUERY}&language={LANGUAGE}&pageSize={PAGE_SIZE}&sortBy=publishedAt&'
    f'apiKey={API_KEY}'
)

#Send request
response = requests.get(url)

# Check response
if response.status_code == 200:
    articles = response.json().get('articles', [])

    # Simplify each article
    simplified_articles = []
    for article in articles:
        simplified_articles.append({
            'title': article['title'],
            'description': article['description'],
            'publishedAt': article['publishedAt'],
            'source': article['source']['name'],
            'url': article['url'],
            'content': article['content']
        })

    # Save as JSON
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(simplified_articles, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(simplified_articles)} articles to {FILENAME}")

else:
    print(f"Failed to fetch news: {response.status_code}")
