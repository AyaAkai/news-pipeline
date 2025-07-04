from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import json
import csv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import subprocess

# DAG default arguments
default_args = {
    'owner': 'aya',
    'start_date': datetime(2025, 7, 2),
    'retries': 1,
}

# News API settings
API_KEY = '7edfaeb8bab2435dabeeadc468506996'
QUERY = 'Egypt'
LANGUAGE = 'en'
PAGE_SIZE = 100

# Function 1: Fetch news from API and save JSON
def fetch_news():
    today = datetime.now().strftime('%Y-%m-%d')
    url = (
        f'https://newsapi.org/v2/everything?'
        f'q={QUERY}&language={LANGUAGE}&pageSize={PAGE_SIZE}&sortBy=publishedAt&'
        f'apiKey={API_KEY}'
    )

    response = requests.get(url)

    if response.status_code == 200:
        articles = response.json().get('articles', [])
        simplified = []

        for article in articles:
            simplified.append({
                'title': article['title'],
                'description': article['description'],
                'publishedAt': article['publishedAt'],
                'source': article['source']['name'],
                'url': article['url'],
                'content': article['content']
            })

        os.makedirs('/home/aya/Desktop/news_project/data/raw', exist_ok=True)
        filepath = f'/home/aya/Desktop/news_project/data/raw/egypt_news_{today}.json'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(simplified, f, ensure_ascii=False, indent=2)

        print(f"Saved {len(simplified)} articles to {filepath}")
    else:
        raise Exception(f"Failed to fetch news: {response.status_code}")

# Function 2: Analyze sentiment and save CSV
def analyze_sentiment():
    today = datetime.now().strftime('%Y-%m-%d')
    input_file = f'/home/aya/Desktop/news_project/data/raw/egypt_news_{today}.json'
    output_dir = '/home/aya/Desktop/news_project/data/processed'
    output_file = f'{output_dir}/egypt_news_sentiment_{today}.csv'

    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as f:
        news_data = json.load(f)

    fields = ['title', 'source', 'publishedAt', 'sentiment', 'sentiment_score']
    analyzer = SentimentIntensityAnalyzer()

    def clean(text):
        if not isinstance(text, str):
            return ''
        return text.replace('"', "'").replace('\n', ' ').replace(',', '،').strip()

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for item in news_data:
            title = clean(item.get('title', ''))
            score = analyzer.polarity_scores(title)
            sentiment = (
                'positive' if score['compound'] >= 0.05 else
                'negative' if score['compound'] <= -0.05 else
                'neutral'
            )

            source_data = item.get('source', '')
            source = clean(source_data.get('name', '') if isinstance(source_data, dict) else source_data)

            writer.writerow({
                'title': title,
                'source': source,
                'publishedAt': clean(item.get('publishedAt', '')),
                'sentiment': sentiment,
                'sentiment_score': score['compound'],
            })

    print(f"Sentiment CSV written to {output_file}")

# Function 3: Upload to S3
def upload_to_s3():
    today = datetime.now().strftime('%Y-%m-%d')
    raw_path = f'/home/aya/Desktop/news_project/data/raw/egypt_news_{today}.json'
    processed_path = f'/home/aya/Desktop/news_project/data/processed/egypt_news_sentiment_{today}.csv'

    raw_s3 = f's3://global-news-sentiment/raw/date={today}/egypt_news_{today}.json'
    processed_s3 = f's3://global-news-sentiment/processed/date={today}/egypt_news_sentiment_{today}.csv'

    subprocess.run(['aws', 's3', 'cp', raw_path, raw_s3], check=True)
    subprocess.run(['aws', 's3', 'cp', processed_path, processed_s3], check=True)

    print("Files uploaded to S3")

# Define DAG
with DAG(
    'newsapi_dag',
    default_args=default_args,
    schedule_interval=None,  
    catchup=False,
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_news',
        python_callable=fetch_news
    )

    analyze_task = PythonOperator(
        task_id='analyze_sentiment',
        python_callable=analyze_sentiment
    )

    upload_task = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3
    )

    fetch_task >> analyze_task >> upload_task

