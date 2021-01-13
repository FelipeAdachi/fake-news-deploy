# fake-news-deploy

Simple Flask web application for fake news detection.
Intended to run on GCP - Cloud Run and stores serving info at BigQuery

- Create a bucket and upload .joblib and .pickle for model and vectorizer
- Create a bigquery table and upload table info at app.py (table_id)
- Replace creds.json with your GCP credentials
- gcloud auth login
- docker build -t fakenewsdeploy:youthful-sponge-32 .
- gcloud builds submit --tag gcr.io/sunny-emissary-293912/fakenewsdeploy:youthful-sponge-32