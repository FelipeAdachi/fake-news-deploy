from google.cloud import bigquery
import os
import datetime
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'


client = bigquery.Client()

###### Table creation (just for first execution)
table_id = 'sunny-emissary-293912.fakenewsdeploy.model_predictions'
schema = [
    bigquery.SchemaField("title", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("content", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("model", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("prediction", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("confidence", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("url", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("prediction_date", "DATETIME", mode="REQUIRED"),

]


table = bigquery.Table(table_id, schema=schema)
table = client.create_table(table)  # API request
print(
    "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
)