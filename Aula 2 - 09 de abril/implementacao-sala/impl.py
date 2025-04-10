import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
df = pd.read_csv("frequencia_notas.csv")

# Considerar apenas alunos presentes e com nota registrada
df_presente = df[(df["Presenca"] == "Sim") & (df["Nota"].notna())]

# Calcular média por aluno
medias_alunos = df_presente.groupby("Aluno", as_index=False)["Nota"].mean()
medias_alunos.rename(columns={"Nota": "Média"}, inplace=True)

# --- Histograma de médias ---
plt.figure(figsize=(8, 4))
medias_alunos["Média"].plot.hist(bins=5, edgecolor='black', color='skyblue')
plt.title("Distribuição das Médias dos Alunos")
plt.xlabel("Média")
plt.ylabel("Quantidade de Alunos")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --- Gráfico de Pizza do Desempenho ---
categorias = ["Aprovados (≥ 7)", "Reprovados (< 7)"]
valores = [
    (medias_alunos["Média"] >= 7).sum(),
    (medias_alunos["Média"] < 7).sum()
]

plt.figure(figsize=(6, 6))
plt.pie(valores, labels=categorias, autopct="%1.1f%%", startangle=90, colors=["#4CAF50", "#F44336"])
plt.title("Desempenho Geral dos Alunos")
plt.axis("equal")  # Deixa a pizza redonda
plt.tight_layout()
plt.show()
