# 📝 Avaliador de Artigos Científicos – NLP em Português

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)]()
[![spaCy](https://img.shields.io/badge/spaCy-pt__core__news__sm-green.svg)]()
[![Status](https://img.shields.io/badge/Status-Ativo-success.svg)]()
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)]()

Este projeto implementa um **avaliador automático de artigos científicos**, capaz de processar textos em português utilizando **Processamento de Linguagem Natural (NLP)**.  
A aplicação fornece uma **API em Python** que analisa a estrutura do texto, identifica possíveis inconsistências e auxilia revisores na triagem inicial de trabalhos acadêmicos.

O projeto foi desenvolvido como trabalho acadêmico sob orientação do **Prof. Dr. Denis Henrique Pinheiro Salvadeo**, com contribuições de **Ana Caroline Silva Pontara** e **Thiago Prado**.

---

## 📌 Funcionalidades Principais

- ✔️ Análise linguística de artigos científicos em português  
- ✔️ Identificação de padrões textuais e alertas de inconsistência  
- ✔️ Verificação automática da estrutura do artigo (Introdução, Método, Resultados, Conclusão etc.)  
- ✔️ API pronta para testes, automações e integrações  
- ✔️ Implementação 100% em Python  

---

## 🚀 Preparação do Ambiente

### 1. Requisitos

- Python **3.8+**
- pip instalado
- Ambiente virtual recomendado

### 2. Criando um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows
### 3. Instalando as Dependências

```bash
pip install -r requirements.txt
```

---

## 🧠 Modelo de Linguagem – spaCy

O projeto depende do modelo **pt_core_news_sm**, essencial para o processamento de textos em português.

Instalação:

```bash
python -m spacy download pt_core_news_sm
```

---

## 🌐 Executando a API

Para iniciar o servidor local:

```bash
uvicorn main:app --reload --port 8000
```

Certifique-se de que a porta **8000** está livre antes de executar.

---

## 🧪 Testando a API

Use **Postman**, **Insomnia**, **cURL** ou qualquer cliente HTTP.

### Exemplo com cURL:

```bash
curl -X POST http://localhost:8000/avaliar \
     -H "Content-Type: application/json" \
     -d '{"texto": "Seu artigo científico aqui..."}'
```

### Exemplo de Resposta (simplificado):

```json
{
  "estrutura": {
    "introducao": "ok",
    "metodologia": "ausente",
    "resultados": "ok",
    "conclusao": "ok"
  },
  "alertas": [
    "Elementos metodológicos insuficientes.",
    "Citações diretas extensas identificadas."
  ]
}
```

---

## 📚 Documentação e Materiais

Este repositório inclui:

* Exemplos detalhados de requisições
* Documentação de uso da API
* Scripts completos da implementação
* Material de apoio disponibilizado pelo professor

---

## 📄 Licença e Atribuição

Este projeto faz parte de um trabalho acadêmico orientado por:

**Prof. Dr. Denis Henrique Pinheiro Salvadeo – UNESP**

Consulte o arquivo **LICENSE** para informações sobre uso e distribuição.

---

## 👩‍💻 Contribuidores

* **Ana Caroline Silva Pontara**
* **Thiago Prado**
