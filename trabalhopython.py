import pandas as pd

# ⿡ Ler o arquivo
df = pd.read_csv("Taxa de mortalidade infantil - Aracaju.csv", sep=";", encoding="latin1")

# ⿢ Filtrar apenas as 3 linhas relevantes
df = df.loc[df["Indicador"].isin([
    "Taxa de mortalidade infantil",
    "Nascidos vivos",
    "Óbitos - Idade menor que 1 ano"
])]

# ⿣ Remover colunas não numéricas (mantendo apenas anos)
anos = [c for c in df.columns if c.isdigit()]
df_long = df.melt(id_vars=["Indicador"], value_vars=anos,
                  var_name="ano", value_name="valor")

# ⿤ Pivotar para cada indicador virar uma coluna
df_pivot = df_long.pivot(index="ano", columns="Indicador", values="valor").reset_index()

print(df_pivot.columns)

# ⿥ Padronizar nomes das colunas
df_pivot.columns = ["ano", "nascidos_vivos", "mortalidade_infantil"]

# ⿦ Converter para números
for col in ["mortalidade_infantil", "nascidos_vivos"]:
    df_pivot[col] = pd.to_numeric(df_pivot[col], errors="coerce")

print(df_pivot.dtypes)

# ⿧ Adicionar nome da cidade
df_pivot["cidade"] = "Aracaju"

# ⿨ Reorganizar colunas
df_pivot = df_pivot[["cidade", "ano", "mortalidade_infantil", "nascidos_vivos"]]

# 🆕 ⿩ Filtrar apenas os anos entre 2010 e 2020
df_pivot["ano"] = df_pivot["ano"].astype(int)
df_pivot = df_pivot[df_pivot["ano"].between(2010, 2020)]

# 🆕 🔟 Salvar o arquivo limpo filtrado
df_pivot.to_csv("mortalidade_aracaju_limpo_2009_2020.csv", index=False, encoding="utf-8-sig")

print("✅ Arquivo limpo salvo como mortalidade_aracaju_limpo_2009_2020.csv")
print(df_pivot)