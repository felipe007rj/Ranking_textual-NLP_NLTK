import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import joblib

def tokenize(text):
    return word_tokenize(text)

def remove_stopwords(words):
    stop_words = set(stopwords.words('english'))
    return [word for word in words if word.lower() not in stop_words]

def apply_lemmatization(words):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words]

def train_similarity_model(df_subset):
    df_subset['tokenized_description'] = df_subset['description'].apply(tokenize)
    df_subset['no_stopwords_description'] = df_subset['tokenized_description'].apply(remove_stopwords)
    df_subset['lemmatized_description'] = df_subset['no_stopwords_description'].apply(apply_lemmatization)
    
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_subset['lemmatized_description'].apply(lambda x: ' '.join(x)))

    svd = TruncatedSVD(n_components=100)
    tfidf_matrix_reduced = svd.fit_transform(tfidf_matrix)

    cosine_similarities_reduced = cosine_similarity(tfidf_matrix_reduced, tfidf_matrix_reduced)

    print("Matriz de Similaridade de Cosseno (Reduzida):")
    print(cosine_similarities_reduced)

    joblib.dump(tfidf_vectorizer, './models/tfidf_vectorizer.joblib')
    joblib.dump(svd, './models/svd_model.joblib')
    joblib.dump(tfidf_matrix_reduced, './models/tfidf_matrix_reduced.joblib')

if __name__ == "__main__":
    df_subset = pd.read_csv('./data/frases.csv')
    df_subset.columns = ['name', 'description']
    train_similarity_model(df_subset)
