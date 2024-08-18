import pandas as pd
import numpy as np


# Carregar a planilha
file_path = 'denguefinder/assets/planilha.xlsx'  # Substitua pelo caminho correto
spreadsheet = pd.ExcelFile(file_path)

# Carregar a planilha "PLANILHA CASOS 2024"
df = pd.read_excel(spreadsheet, sheet_name='PLANILHA CASOS 2024')

# Ajustar o DataFrame, definindo a primeira linha como cabeçalho e removendo colunas vazias
df.columns = df.iloc[0]
df = df[1:]
df = df.dropna(axis=1, how='all')

# Renomear as colunas de interesse
df = df.rename(columns={'BAIRRO': 'Bairro', 'RESULTADO': 'Resultado'})

# Contagem de casos notificados por bairro
casos_notificados = df['Bairro'].value_counts().reset_index()
casos_notificados.columns = ['Bairro', 'Casos_Notificados']

# Contagem de casos positivos por bairro
casos_positivos = df[df['Resultado'].str.contains(
    'POSITIVO', na=False)]['Bairro'].value_counts().reset_index()
casos_positivos.columns = ['Bairro', 'Casos_Positivos']

# Contagem de casos negativos por bairro
casos_negativos = df[df['Resultado'].str.contains(
    'NEGATIVO', na=False)]['Bairro'].value_counts().reset_index()
casos_negativos.columns = ['Bairro', 'Casos_Negativos']

# Mesclar os DataFrames em um único DataFrame
df_final = casos_notificados.merge(casos_positivos, on='Bairro', how='left').merge(
    casos_negativos, on='Bairro', how='left')

# Preencher valores NaN com 0 (casos onde não há registros positivos ou negativos)
df_final = df_final.fillna(0)

# Converter os valores de casos para inteiros
df_final['Casos_Positivos'] = df_final['Casos_Positivos'].astype(int)
df_final['Casos_Negativos'] = df_final['Casos_Negativos'].astype(int)

# Função para ajustar os números aleatoriamente entre -10 e +10


def ajustar_numero(numero):
    ajuste = np.random.randint(-10, 11)
    return max(0, numero + ajuste)


# Aplicar a função para ajustar os números
df_final['Casos_Notificados'] = df_final['Casos_Notificados'].apply(
    ajustar_numero)
df_final['Casos_Positivos'] = df_final['Casos_Positivos'].apply(ajustar_numero)
df_final['Casos_Negativos'] = df_final['Casos_Negativos'].apply(ajustar_numero)

# Adicionar colunas de coordenadas com valor inicial 0
df_final['latitude'] = 0.0
df_final['longitude'] = 0.0

# Converter o DataFrame para JSON
json_data = df_final.to_json(orient='records', force_ascii=False)

# Salvar o JSON em um arquivo
output_file = 'denguefinder/assets/casos_por_bairro_ajustados.json'
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(json_data)

print(f"JSON salvo em: {output_file}")
