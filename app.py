from flask import Flask, request, render_template, jsonify
from boilerpy3 import extractors
import os
from download_model import download_model_from_gcp
from preprocess import denoise_text
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from joblib import load
import datetime
import numpy as np
from google.cloud import bigquery

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'

extractor = extractors.ArticleExtractor()

app = Flask(__name__)
models_folder = "models"
model_name = "youthful-sponge-32"
download_model_from_gcp(model_name)

client = bigquery.Client()
table_id = 'sunny-emissary-293912.fakenewsdeploy.model_predictions'
table = client.get_table(table_id)  # API request


@app.route('/')
def my_form():
    return render_template('url_form.html')

@app.route('/', methods=['POST'],defaults = {'from_home':True})
@app.route('/api/classify_news', methods=['POST'], defaults = {'from_home' : False})
def classify_news(from_home):
    if from_home:
        news_url = request.form['text']
    else:
        news_url = request.json['text']

    content,title = read_content_from_url(news_url)
    content_tfidf,coverage,word_count = preprocess_and_transform(content,title)
    predicted_str,confidence = predict_fake_news(content_tfidf)

    to_insert = {
        'title': title,
        'content': content,
        'model': model_name,
        'prediction': predicted_str,
        'confidence': confidence,
        'url': news_url,
        'prediction_date': datetime.datetime.now(),
        'coverage': coverage,
        'word_count': word_count

    }
    insert_to_bigquery(to_insert)
    if from_home:
        display = """
        <h1 >{}</h1>
        <p>This news is probably <b>{}</b>!</p>
        <p>Prediction confidence: {}</p>
        """.format(title,predicted_str,confidence)
        return display
    else:
        to_return = to_insert
        return jsonify(to_return)

def read_content_from_url(news_url):
    doc = extractor.get_doc_from_url(news_url)
    content = doc.content
    title = doc.title
    return content,title

def preprocess_and_transform(content,title):
    content = content + " " + title
    content = denoise_text(content)
    
    feature_path = os.path.join(models_folder,model_name,"feature_{}.pickle".format(model_name))
    count_vect = CountVectorizer(decode_error="replace",vocabulary=pickle.load(open(feature_path, "rb")))

    #Get word coverage
    tokenizer = count_vect.build_tokenizer()
    feature_vocab = count_vect.get_feature_names()
    feature_content = tokenizer(content)
    word_count = len(feature_content)
    intesection = [x for x in feature_content if x in feature_vocab]
    coverage = len(intesection)/len(feature_content)

    tfidf_transformer = TfidfTransformer()
    content_counts = count_vect.transform([content])
    content_tfidf = tfidf_transformer.fit_transform(content_counts)

    return content_tfidf,coverage,word_count

def predict_fake_news(content_tfidf):
    model_path = os.path.join(models_folder,model_name,"{}.joblib".format(model_name))
    clf = load(model_path)
    preds = clf.predict_proba(content_tfidf) 
    predicted = np.argmax(preds[0])
    predicted_str = 'Real' if predicted == 1 else 'Fake'
    confidence = preds[0][predicted]

    return predicted_str,confidence

def insert_to_bigquery(to_insert):
    global table
    rows_to_insert = [to_insert]
    errors = client.insert_rows(table, rows_to_insert)  # API request
    assert errors == []



if __name__ == '__main__':
    # app.run()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
