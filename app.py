from flask import Flask, request, render_template
from boilerpy3 import extractors

extractor = extractors.ArticleExtractor()

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('url_form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    news_url = request.form['text']
    doc = extractor.get_doc_from_url(news_url)
    content = doc.content
    title = doc.title
    return title

if __name__ == '__main__':
    # app.run()
    app.run(debug=True, host='0.0.0.0', port=80)
