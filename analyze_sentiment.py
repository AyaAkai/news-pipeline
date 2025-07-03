import json
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

input_file = 'data/egypt_news_2025-07-02.json'
output_file = 'data/newsv.csv'

# تم حذف 'date' من الـ fields
fields = ['title', 'source', 'publishedAt', 'sentiment', 'sentiment_score']
analyzer = SentimentIntensityAnalyzer()

def clean_field(text):
    if not isinstance(text, str):
        return ''
    text = text.replace('"', "'").replace('\n', ' ').replace(',', '،')
    return text.strip()

with open(input_file, 'r', encoding='utf-8') as f:
    news_data = json.load(f)

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields, quoting=csv.QUOTE_ALL)
    writer.writeheader()

    total = 0
    written = 0

    for item in news_data:
        total += 1
        title = clean_field(item.get('title', ''))
        score = analyzer.polarity_scores(title)
        sentiment = (
            'positive' if score['compound'] >= 0.05 else
            'negative' if score['compound'] <= -0.05 else
            'neutral'
        )

        source_data = item.get('source', '')
        source = clean_field(source_data.get('name', '') if isinstance(source_data, dict) else source_data)

        row = {
            'title': title,
            'source': source,
            'publishedAt': clean_field(item.get('publishedAt', '')),
            'sentiment': sentiment,
            'sentiment_score': score['compound'],
        }

        if len(row) == len(fields):
            try:
                writer.writerow(row)
                written += 1
            except Exception as e:
                print(f"Skipping row due to write error: {e}")

print(f"{written} out of {total} rows written to {output_file}")
