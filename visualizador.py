import argparse
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

# Argumentos CLI
parser = argparse.ArgumentParser(
    description="Visualização de frequência de palavras por categoria gramatical"
)
parser.add_argument(
    "--csv", type=str, required=True,
    help="Arquivo CSV anotado com Token, Lema, POS ou já agregados com coluna 'Frequência'"
)
parser.add_argument(
    "--limite", type=int, default=30,
    help="Número de itens a exibir nos gráficos"
)
parser.add_argument(
    "--tipo", choices=["substantivo", "verbo", "adjetivo"], required=True,
    help="Tipo morfossintático: substantivo, verbo, adjetivo"
)
parser.add_argument(
    "--grafico", choices=["bar", "cloud"], required=True,
    help="Tipo de gráfico: bar (barras) ou cloud (nuvem)"
)
parser.add_argument(
    "--formato", choices=["png", "svg", "pdf"], default="png",
    help="Formato de saída do gráfico"
)
args = parser.parse_args()

# Carregamento do CSV
data_file = args.csv
try:
    df = pd.read_csv(data_file)
except FileNotFoundError:
    print(f"❌ Arquivo não encontrado: {data_file}")
    exit(1)

# Mapeamento do tipo morfossintático
mapa_tipo = {
    "substantivo": "NOUN",
    "verbo":      "VERB",
    "adjetivo":   "ADJ",
}
tipo_pos = mapa_tipo[args.tipo]

# 🔎 Filtragem de POS e preparação de Frequências
mask = df['POS'] == tipo_pos
df_filtrado = df.loc[mask].copy()
# Normaliza lemmas
df_filtrado['Lema'] = df_filtrado['Lema'].astype(str).str.lower().str.strip()
# Remove registros vazios
df_filtrado = df_filtrado[df_filtrado['Lema'].ne('') & df_filtrado['Lema'].notna()]

# Computa série de frequências
if 'Frequência' in df_filtrado.columns:
    # CSV já possui coluna de frequência agregada
    freq_series = df_filtrado.set_index('Lema')['Frequência'].astype(int)
    freq_series = freq_series.groupby(level=0).sum().sort_values(ascending=False)
else:
    # conta ocorrências de lemma
    freq_series = df_filtrado['Lema'].value_counts()

# Top N
top = freq_series.head(args.limite)
lemas = top.index.tolist()
frequencias = top.values.tolist()

# Extensão de saída
ext = args.formato

# Gráfico de barras
if args.grafico == 'bar':
    plt.figure(figsize=(12, 8))
    bars = plt.barh(lemas[::-1], frequencias[::-1], color='#4c72b0')
    plt.xlabel('Frequência')
    plt.title(f"Top {args.limite} {args.tipo.upper()}S mais frequentes")
    maxf = max(frequencias) if frequencias else 1
    plt.xlim(0, maxf * 1.1)
    # rótulo ao final de cada barra
    for bar, freq in zip(bars, frequencias[::-1]):
        x = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        plt.text(x + maxf * 0.01, y, str(freq), va='center')
    plt.tight_layout()
    out_file = f"top_{args.tipo}_{args.limite}.{ext}"
    plt.savefig(out_file)
    plt.show()
    print(f"📦 Exportado: {out_file}")

# Nuvem de palavras
elif args.grafico == 'cloud':
    # usa apenas o top N definido em top
    top_dict = dict(zip(lemas, frequencias))
    wc = WordCloud(width=1000, height=600, background_color='white', colormap='viridis')
    wc.generate_from_frequencies(top_dict)
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"Nuvem de Palavras: {args.tipo.upper()}S")
    plt.tight_layout()
    out_file = f"nuvem_{args.tipo}.{ext}"
    plt.savefig(out_file)
    plt.show()
    print(f"📦 Exportado: {out_file}")
