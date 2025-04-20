import stanza
import re
import pandas as pd
import argparse
from collections import Counter

# Argumentos CLI
parser = argparse.ArgumentParser(description="Frequência de lemas com POS no De Bello Gallico")
parser.add_argument("--no-stopwords", action="store_true", help="Remove stopwords latinas do resultado")
args = parser.parse_args()

# Carrega texto
with open("de_bello_gallico.txt", "r", encoding="utf-8") as f:
    texto = f.read()

# Limpeza
def pre_processamento(texto):
    texto = re.sub(r"\b[ADFIKLMNOPRUVX]+\.\b", "", texto)
    texto = re.sub(r"[^\w\sāēīōūæœ]", " ", texto)
    texto = re.sub(r"\d+", "", texto)
    texto = re.sub(r"\s{2,}", " ", texto)
    return texto.strip()

texto_limpo = pre_processamento(texto)

# NLP
stanza.download('la')  # só na primeira vez
nlp = stanza.Pipeline(lang='la', processors='tokenize,mwt,pos,lemma', use_gpu=False)

print("⏳ Analisando texto...")
doc = nlp(texto_limpo)
print("✔️ Análise concluída.")

# Lista expandida de stopwords
stopwords_latinas = {
    "et", "in", "de", "cum", "ad", "per", "a", "ab", "ex", "sub", "sed", "ut",
    "non", "autem", "nam", "ne", "nec", "vel", "enim", "atque", "quoque",
    "quod", "quia", "si", "quoniam", "dum", "postquam", "antequam", "ubi",
    "ita", "tamen", "ergo", "inter", "contra", "propter", "super",
    "is", "hic", "ille", "qui", "quae", "quod", "quis", "ut", "an", "aut",
    "etiam", "tamen", "igitur", "sum", "esse", "fui", "possum", "idem",
    "ipse", "quidem", "meus", "tuus", "suus", "noster", "vester", "se", "sui",
    "ego", "nos", "tu", "vos"
}

# Token válido
def is_token_valido(word):
    return (
        word.lemma and
        word.upos not in {"PUNCT", "SYM", "NUM", "X"} and
        re.match(r"^[a-zA-Zāēīōūæœ]+$", word.lemma)
    )

# Extração com POS
tokens_filtrados = [
    (word.lemma.lower(), word.upos)
    for sent in doc.sentences
    for word in sent.words
    if is_token_valido(word)
]

# Remove stopwords se necessário
if args.no_stopwords:
    tokens_filtrados = [
        (lemma, pos) for (lemma, pos) in tokens_filtrados
        if lemma not in stopwords_latinas
    ]
    print("🧹 Stopwords removidas.")

# Frequência com POS
frequencia = Counter(tokens_filtrados)
frequentes = [(lema, pos, freq) for (lema, pos), freq in frequencia.items() if freq >= 5]

# Exporta CSV
sufixo = "_sem_stopwords" if args.no_stopwords else "_com_stopwords"
df = pd.DataFrame(frequentes, columns=["Lema", "POS", "Frequência"]).sort_values(by="Frequência", ascending=False)
df.to_csv(f"lemas_freq{sufixo}.csv", index=False)
print(f"📄 Arquivo gerado: lemas_freq{sufixo}.csv")
