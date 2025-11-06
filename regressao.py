import pandas as pd
import statsmodels.api as sm

# === 1. Carregar os dois arquivos já limpos ===
df_mortalidade = pd.read_csv("mortalidade_aracaju_limpo.csv")
df_esf = pd.read_csv("cobertura_esf_media_anual.csv")

# === 2. Unir as bases pelo ano ===
df_merged = pd.merge(df_mortalidade, df_esf, on="ano", how="inner")

print("\n🔗 Dados combinados (pré-regressão):")
print(df_merged.head())

# === 3. Regressão linear: mortalidade_infantil ~ cobertura_esf ===
X = df_merged["media_cobertura_esf"]   # variável independente
y = df_merged["mortalidade_infantil"]  # variável dependente

# Adiciona constante ao modelo
X = sm.add_constant(X)

# Cria e ajusta o modelo
modelo = sm.OLS(y, X).fit()

# === 4. Exibir resultados ===
print("\n📊 RESULTADOS DA REGRESSÃO:")
print(modelo.summary())

# === 5. (Opcional) Salvar base combinada ===
df_merged.to_csv("base_final_aracaju.csv", index=False, encoding="utf-8-sig")
print("\n💾 Base final salva como 'base_final_aracaju.csv'")