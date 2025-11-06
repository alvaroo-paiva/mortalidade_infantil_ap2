import pandas as pd
import glob
import os

# === LER E UNIR TODOS OS ARQUIVOS ===

# Pega todos os arquivos Excel da pasta atual
arquivos = glob.glob("*.xlsx")

# Lista para armazenar os DataFrames
dados = []

for arquivo in arquivos:
    try:
        # Extrai o ano do nome do arquivo (número de 4 dígitos)
        ano = int(''.join([c for c in arquivo if c.isdigit()][:4]))
        
        # Lê o arquivo Excel
        df = pd.read_excel(arquivo)

        # Localiza a coluna correta de cobertura ESF
        colunas = [c for c in df.columns if "Cobertura" in c and "ESF" in c]
        if not colunas:
            print(f"⚠ Coluna não encontrada em {arquivo}")
            continue

        # Renomeia para nome padrão
        df = df.rename(columns={colunas[0]: "cobertura_esf"})

        # Mantém apenas a coluna desejada
        df = df[["cobertura_esf"]].copy()

        # Corrige formato numérico
        df["cobertura_esf"] = (
            df["cobertura_esf"]
            .astype(str)
            .str.replace(".", "", regex=False)   # remove separador de milhar
            .str.replace(",", ".", regex=False)  # troca vírgula por ponto
        )
        df["cobertura_esf"] = pd.to_numeric(df["cobertura_esf"], errors="coerce")

        # Adiciona colunas de ano e município
        df["ano"] = ano
        df["municipio"] = "Aracaju"

        dados.append(df)
        print(f"✅ Arquivo {arquivo} lido com sucesso (ano {ano})")

    except Exception as e:
        print(f"❌ Erro ao processar {arquivo}: {e}")

# === COMBINAR TODOS OS ANOS ===
if dados:
    df_final = pd.concat(dados, ignore_index=True)
    df_final = df_final.sort_values("ano").reset_index(drop=True)
    print("\n✅ Dados combinados com sucesso!")
    print(df_final[["ano", "cobertura_esf"]].head(20))

    # Salva o arquivo combinado
    df_final.to_csv("cobertura_esf_aracaju_2009_2020.csv", index=False, encoding="utf-8-sig")
    print("💾 Arquivo salvo como 'cobertura_esf_aracaju_2009_2020.csv'")

    # === AGRUPAR OS DADOS POR ANO (MÉDIA ANUAL) ===
    # Agrupar por ano e calcular a média da cobertura ESF
    df_media_anual = (
        df_final.groupby("ano", as_index=False)["cobertura_esf"].mean()
    )

    # Renomear a coluna para ficar mais legível
    df_media_anual.rename(columns={"cobertura_esf": "media_cobertura_esf"}, inplace=True)

    # Exibir o resultado
    print("\n📊 Média anual da cobertura ESF:")
    print(df_media_anual)

    # Salvar o resultado em CSV
    df_media_anual.to_csv("cobertura_esf_media_anual.csv", index=False, encoding="utf-8-sig")
    print("💾 Arquivo 'cobertura_esf_media_anual.csv' criado com sucesso!")
