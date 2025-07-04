# news-pipeline

# 📰 Global News Sentiment Analysis Pipeline

This project builds a **fully automated data engineering pipeline** that collects, analyzes, and stores global news data about Egypt, enriched with sentiment insights. It integrates **Python**, **Apache Airflow**, **AWS**, and **Power BI**, forming a real-world, production-style solution.

---

## 📌 Project Objective

To automate the **collection, sentiment analysis, cloud storage, and dashboard visualization** of daily global news related to Egypt, enabling real-time monitoring of public opinion trends.

---

## 🧱 Architecture Overview

The pipeline consists of:

1. **News API Integration**: Fetches latest Egypt-related news using [NewsAPI](https://newsapi.org/).
2. **Sentiment Analysis**: Applies `VADER` (Valence Aware Dictionary for sEntiment Reasoning) to analyze titles.
3. **ETL Orchestration**: Airflow DAG automates fetching, processing, and uploading the data.
4. **Cloud Storage**: Files are saved in AWS S3 — structured as `raw/` and `processed/` layers.
5. **Visualization**: Power BI report (import mode) connects to AWS S3 via ODBC for dynamic insights.

---

## 🛠️ Tools & Technologies

| Tool            | Purpose                                  |
|-----------------|-------------------------------------------|
| Python          | Core scripting and sentiment analysis     |
| Airflow         | Workflow orchestration                    |
| NewsAPI         | News data source                          |
| AWS S3          | Cloud storage                             |
| Power BI        | Data visualization                        |
| VADER Sentiment | NLP-based sentiment scoring               |
| GitHub          | Version control and collaboration         |

---

## 🗂️ Project Structure

```

news\_project/
│
├── dags/                          # Airflow DAGs
│   └── newsapi\_dag.py
│
├── data/
│   ├── raw/                       # Raw news JSON files
│   ├── processed/                 # Sentiment-analyzed CSV files
│
├── scripts/                       # Optional Python helpers
│
└── README.md                      # Project documentation

```

---

## 🔄 DAG Workflow in Airflow

The DAG runs **weekly every Wednesday at 6 PM** and performs:

1. `fetch_news`: Queries NewsAPI and stores news as JSON in S3.
2. `analyze_sentiment`: Applies VADER to generate CSVs with sentiment.
3. `upload_to_s3`: Uploads both raw and processed data to AWS S3.

---

## 📊 Power BI Report

The final dashboard includes:

- Sentiment distribution pie chart
- Time-series trends
- Top positive & negative headlines
- Word cloud of frequent terms
- Source-level sentiment comparison

All visuals update upon weekly ingestion & processing.

---

## 🌐 Deployment Notes

- DAGs live in: `/home/aya/Desktop/news_project/dags`
- S3 bucket: `s3://global-news-sentiment`
- Airflow is triggered via a local venv `airflow_env`
- Power BI uses import mode via ODBC Athena DSN

---

## 🎯 Key Learning Outcomes

- Real-world DAG orchestration using Airflow
- Managing multi-layered data pipelines with AWS
- Applying sentiment analysis using NLP
- Visual storytelling with Power BI

---

## ✅ Status

🟢 **Completed**  
All components work end-to-end with weekly automated refresh and a ready-for-demo dashboard.

---

## 🚀 Final Note

This project showcases a **fully automated news sentiment analysis pipeline** — from API ingestion to AWS cloud storage, orchestrated via Apache Airflow and visualized in Power BI. Ready to scale, adapt, and inspire.

💡 Feel free to fork, adapt, or extend this project for your own use case. Built to be modular, educational, and practical.
```
