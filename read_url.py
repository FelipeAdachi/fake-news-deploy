from boilerpy3 import extractors

extractor = extractors.ArticleExtractor()

# From a URL
# content = extractor.get_content_from_url('https://www.reuters.com/article/us-usa-court-barrett/democrats-focus-on-obamacare-fate-at-trump-supreme-court-nominees-hearing-idUSKBN26X17X')

# print(content)


doc = extractor.get_doc_from_url('https://www.reuters.com/article/us-usa-court-barrett/democrats-focus-on-obamacare-fate-at-trump-supreme-court-nominees-hearing-idUSKBN26X17X')
content = doc.content
title = doc.title

print(title)