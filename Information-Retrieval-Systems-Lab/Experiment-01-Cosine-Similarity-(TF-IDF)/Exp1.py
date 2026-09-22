#24BQ1A42W4
#SOLLAPUR SAI AVINASH REDDY
from sklearn.feature_extraction.text import TfidfVectorizer

# Define placeholder documents. Replace with your actual text data.
doc1 = "This is the first document."
doc2 = "This document is the second document."

vectorizer = TfidfVectorizer(stop_words= 'english')
tfidf_matrix = vectorizer.fit_transform([doc1 , doc2])


from sklearn.metrics.pairwise import cosine_similarity

similarity  = cosine_similarity(tfidf_matrix[0:1] , tfidf_matrix[1:2])

print(f"Cosine similarity : {similarity[0][0]:.4f}")
