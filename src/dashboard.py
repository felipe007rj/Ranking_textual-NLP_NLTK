import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_dashboard(df_sorted):
    # Configurações globais
    app = dash.Dash(__name__)
    app.title = 'Dashboard Empresarial'

    # Layout do aplicativo
    app.layout = html.Div([
        html.H1("Dashboard Empresarial", style={'text-align': 'center', 'background-color': 'dimgray', 'color': 'white', 'padding': '20px'}),
        
        # Gráfico de Distribuição de Funcionários
        html.Div([
            dcc.Graph(
                id='histogram-employees',
                figure={
                    'data': [
                        {'x': df_sorted['employees'].dropna(), 'type': 'histogram', 'name': 'Funcionários'}
                    ],
                    'layout': {
                        'title': 'Distribuição de Funcionários por Empresa',
                        'xaxis': {'title': 'Número de Funcionários'},
                        'yaxis': {'title': 'Contagem de Empresas', 'type': 'log'},
                        'plot_bgcolor': 'lightgray',  # Adiciona o fundo cinza claro
                    }
                }
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        # Gráfico de Distribuição de Similaridade
        html.Div([
            dcc.Graph(
                id='histogram-similarity',
                figure={
                    'data': [
                        {'x': df_sorted['similaridade'], 'type': 'histogram', 'name': 'Similaridade', 'marker': {'color': 'salmon'}}
                    ],
                    'layout': {
                        'title': 'Distribuição de Similaridade entre Empresas',
                        'xaxis': {'title': 'Similaridade'},
                        'yaxis': {'title': 'Contagem de Empresas'},
                        'plot_bgcolor': 'lightgray',  # Adiciona o fundo cinza claro
                    }
                }
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        # Gráfico de Dispersão entre Funcionários e Similaridade
        html.Div([
            dcc.Graph(
                id='scatter-employees-similarity',
                figure={
                    'data': [
                        {'x': df_sorted['employees'], 'y': df_sorted['similaridade'], 'mode': 'markers', 'type': 'scatter', 'marker': {'opacity': 0.7}}
                    ],
                    'layout': {
                        'title': 'Relação entre Funcionários e Similaridade',
                        'xaxis': {'title': 'Número de Funcionários'},
                        'yaxis': {'title': 'Similaridade'},
                        'plot_bgcolor': 'lightgray',  # Adiciona o fundo cinza claro
                    }
                }
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        # Gráfico de Barras para as Top 10 Cidades
        html.Div([
            dcc.Graph(
                id='bar-top-cities',
                figure={
                    'data': [
                        {'x': df_sorted['city'].value_counts().head(10).index, 'y': df_sorted['city'].value_counts().head(10).values, 'type': 'bar', 'marker': {'color': 'viridis'}}
                    ],
                    'layout': {
                        'title': 'Top 10 Cidades (Pólos de Desenvolvimento)',
                        'xaxis': {'title': 'Cidade'},
                        'yaxis': {'title': 'Número de Empresas'},
                        'plot_bgcolor': 'lightgray',  # Adiciona o fundo cinza claro
                    }
                }
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),
    ])

    return app

if __name__ == '__main__':
    df = pd.read_csv('./data/watersimilar.csv')
    # Removendo linhas com valores nulos e 0 na coluna 'employees' e convertendo para tipos numéricos
    df = df[(df['employees'].notna()) & (df['employees'] != 0)]
    df['employees'] = pd.to_numeric(df['employees'], errors='coerce')

    # Ordenando o DataFrame pelo número de funcionários (do menor para o maior) e removendo linhas com valor 0
    df_sorted = df[df['employees'] != 0].sort_values(by='employees')

    # Gerando o dashboard
    dashboard_app = generate_dashboard(df_sorted)

    # Executando o aplicativo
    dashboard_app.run_server(debug=True)
