import pandas as pd
from src.preprocess import preprocess_data
from src.treino_similaridade import train_similarity_model
from src.inferencia_similaridade import calculate_similarity

def main():
    file_path = './data/canada.xlsm'
    
    # Pré-processamento
    df_subset = preprocess_data(file_path)
    
    # Treino do modelo de similaridade
    train_similarity_model(df_subset)
    
    # Inferência usando o modelo treinado
    new_description = "solutions on waste and water, Improve water quality and water efficiency use, water contamination, water for human consumption, water resources"
    calculate_similarity(df_subset, new_description, top_n=10)

if __name__ == "__main__":
    main()
