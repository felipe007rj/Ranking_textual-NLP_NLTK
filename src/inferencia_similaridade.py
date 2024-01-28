
import joblib
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

def tokenize(text):
    return word_tokenize(text)

def remove_stopwords(words):
    stop_words = set(stopwords.words('english'))
    return [word for word in words if word.lower() not in stop_words]

def apply_lemmatization(words):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words]

def calculate_similarity(df_subset, new_description, top_n=10):
    tfidf_vectorizer = joblib.load('./models/tfidf_vectorizer.joblib')
    svd = joblib.load('./models/svd_model.joblib')
    tfidf_matrix_reduced = joblib.load('./models/tfidf_matrix_reduced.joblib')

    # Pré-processamento da nova descrição
    tokenized_description = tokenize(new_description)
    no_stopwords_description = remove_stopwords(tokenized_description)
    lemmatized_description = apply_lemmatization(no_stopwords_description)

    # Codificação de Texto usando TF-IDF e redução de dimensionalidade
    new_tfidf_matrix = tfidf_vectorizer.transform([' '.join(lemmatized_description)])
    new_tfidf_matrix_reduced = svd.transform(new_tfidf_matrix)

    # Calculando similaridade de cosseno entre a nova descrição e as existentes
    similarity_scores = cosine_similarity(new_tfidf_matrix_reduced, tfidf_matrix_reduced)
    
    # Obtendo os índices das 10 maiores pontuações
    top_indices = similarity_scores.argsort()[0, ::-1][:top_n]

    # Extraindo os nomes e descrições mais similares
    top_names = df_subset['name'].iloc[top_indices]
    top_descriptions = df_subset['description'].iloc[top_indices]
    top_similarity_scores = similarity_scores[0, top_indices]

    # Exibindo os resultados
    print(f"Nova Descrição: {new_description}")
    print("\nTop 10 Frases Mais Similares:")
    for name, description, score in zip(top_names, top_descriptions, top_similarity_scores):
        print(f"Nome da Empresa: {name}")
        print(f"Descrição Mais Similar: {description}")
        print(f"Pontuação de Similaridade: {score}\n")

if __name__ == "__main__":
    df_subset = pd.read_csv('./data/frases.csv')
    df_subset.columns = ['name', 'description']

    # Exemplo de uso da função com uma nova descrição
    new_description = "solutions on waste and water, Improve water quality and water efficiency use, water contamination, water for human consumption, water resources"
    calculate_similarity(df_subset, new_description, top_n=10)
