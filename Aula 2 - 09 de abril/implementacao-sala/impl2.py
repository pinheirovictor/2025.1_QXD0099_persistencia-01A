import pandas as pd
import matplotlib.pyplot as plt

# 1. Carregar o CSV com os dados de presença e notas
df = pd.read_csv("frequencia_notas.csv")  # Certifique-se de que o caminho esteja correto


# 2. Mostrar o DataFrame completo
print(df)
print(df.head())  # Mostra as 5 primeiras linhas
print(df.head(10))  # Mostra as 10 primeiras
print(df.info())  # Tipos de dados, colunas e valores nulos
print(df.describe())  # Média, desvio padrão, min, max, etc.


# =====================================================================
# 2. Cálculo da frequência por aluno

# Converter a coluna "Presenca" para valores binários (Sim = 1, Não = 0)
df["Presenca_Bin"] = df["Presenca"].map({"Sim": 1, "Não": 0})

# Calcular o total de aulas registradas por aluno
total_aulas = df.groupby("Aluno")["Presenca_Bin"].count().reset_index(name="Total_Aulas")

# Calcular o número de presenças por aluno
presencas = df.groupby("Aluno")["Presenca_Bin"].sum().reset_index(name="Presencas")

# Juntar os dois DataFrames para calcular a frequência
frequencia = pd.merge(total_aulas, presencas, on="Aluno")


# Calcular a frequência em porcentagem
frequencia["Frequencia (%)"] = (frequencia["Presencas"] / frequencia["Total_Aulas"]) * 100

# Associar o curso a cada aluno (assumindo que é o mesmo curso em todas as linhas de um aluno)
cursos = df[["Aluno", "Curso"]].drop_duplicates()
frequencia = pd.merge(frequencia, cursos, on="Aluno")

# =====================================================================
# 3. Cálculo da média de notas por aluno (considerando apenas as aulas em que o aluno estava presente)

# Filtrar apenas as linhas com presença "Sim" e nota não nula
notas_validas = df[(df["Presenca"] == "Sim") & (df["Nota"].notna())]

# Calcular a média de notas por aluno
medias = notas_validas.groupby("Aluno")["Nota"].mean().reset_index(name="Media")

# =====================================================================
# 4. Identificar alunos em risco (baixa frequência ou baixa média)

# Juntar os dados de frequência e média
resumo = pd.merge(frequencia, medias, on="Aluno", how="left")

# Selecionar alunos com frequência menor que 75% ou média menor que 6
alunos_em_risco = resumo[(resumo["Frequencia (%)"] < 75) | (resumo["Media"] < 6)]

# Salvar a lista de alunos em risco em um CSV
alunos_em_risco.to_csv("alunos_em_risco.csv", index=False)

# =====================================================================
# 5. Salvar os resultados gerais em arquivos

# Salvar o resumo completo em CSV
resumo.to_csv("frequencia_geral.csv", index=False)

# Calcular a média de notas por curso
media_por_curso = pd.merge(resumo[["Aluno", "Media"]], cursos, on="Aluno")
media_por_curso = media_por_curso.groupby("Curso")["Media"].mean().reset_index()

# Salvar a média por curso em um arquivo Excel
media_por_curso.to_excel("media_por_curso.xlsx", index=False)

# Visualizações Gráficas

import matplotlib.pyplot as plt

# 1. Gráfico de barras mostrando a frequência de cada aluno
plt.figure(figsize=(12, 6))
plt.bar(resumo["Aluno"], resumo["Frequencia (%)"], color='skyblue')
plt.xticks(rotation=90)  # Rotaciona os nomes dos alunos para melhor visualização
plt.title("Frequência por Aluno (%)")
plt.xlabel("Aluno")
plt.ylabel("Frequência (%)")
plt.tight_layout()
plt.savefig("frequencia_por_aluno.png")  # Salva o gráfico como imagem
plt.close()

# 2. Gráfico de pizza mostrando a distribuição das faixas de notas

# Função para categorizar as notas em faixas (A, B, C, D)
def categoria(nota):
    if pd.isna(nota):
        return "Sem Nota"
    elif nota >= 9:
        return "A"
    elif nota >= 7:
        return "B"
    elif nota >= 5:
        return "C"
    else:
        return "D"

# Aplicar a função para criar uma nova coluna com a faixa de cada aluno
resumo["Faixa"] = resumo["Media"].apply(categoria)

# Contar quantos alunos estão em cada faixa
contagem = resumo["Faixa"].value_counts()

# Criar o gráfico de pizza
plt.figure(figsize=(6, 6))
plt.pie(contagem, labels=contagem.index, autopct="%1.1f%%", startangle=90)
plt.title("Distribuição por Faixa de Nota")
plt.axis("equal")  # Deixa o gráfico redondo
plt.tight_layout()
plt.savefig("distribuicao_faixas_nota.png")  # Salva o gráfico como imagem
plt.close()


