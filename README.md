# 📚 Caesar Textmining – Frequência e Visualização de Lemas Latinos

Este repositório contém dois scripts em Python para processamento, análise de frequência e visualização de lemas do *De Bello Gallico*, utilizando NLP para Latim com a biblioteca [Stanza](https://stanfordnlp.github.io/stanza/).

---

## 📂 Estrutura

- `frequencia.py`: Gera arquivo CSV com frequência de lemas e POS tagging.
- `visualizador.py`: Gera gráficos e nuvem de palavras a partir do CSV.

---

## 🛠️ Requisitos

### 1. Clone o repositório:
```bash
git clone https://github.com/LeoVichi/caesar_freq
cd caesar_freq
```

### 2. Crie e ative um ambiente virtual Python:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências com:

```bash
pip install -r requirements.txt
```

## 📥 Uso

### 1. Geração de Frequência

```bash
python frequencia.py [--no-stopwords]
```

- `--no-stopwords`: Remove stopwords latinas antes da contagem.

Gera:
- `lemas_freq_com_stopwords.csv`
- ou `lemas_freq_sem_stopwords.csv`

---

### 2. Visualização

```bash
python visualizador.py --csv lemas_freq_com_stopwords.csv --tipo verbo --grafico bar --limite 20 --formato png
```

#### Argumentos obrigatórios:

- `--csv`: Caminho para o arquivo CSV gerado.
- `--tipo`: Tipo da categoria gramatical (`substantivo`, `verbo`, `adjetivo`).
- `--grafico`: Tipo de gráfico (`bar` ou `cloud`).

#### Argumentos opcionais:

- `--limite`: Quantos lemas exibir (padrão: 30).
- `--formato`: Formato do gráfico (`png`, `svg`, `pdf`).

---

## ✨ Exemplo

```bash
python frequencia.py --no-stopwords
python visualizador.py --csv lemas_freq_sem_stopwords.csv --tipo substantivo --grafico cloud
```

---

## 🧑‍💻 Autor

**Leonardo Vichi**  
Desenvolvido por [Leonardo Vichi](https://github.com/LeoVichi) para atividade de Estágio Pós-Doutoral junto ao Programa de Pós-Graduação em Letras Clássicas da Universidade Federal do Rio de Janeiro - PPGLC/UFRJ.

---

## ⚖️ Licença

Distribuído sob a licença [MIT](https://opensource.org/licenses/MIT).
