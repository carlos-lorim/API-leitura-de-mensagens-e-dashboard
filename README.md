# 📨 API de Leitura de Mensagens & Dashboard de Atendimento

> Sistema inteligente de triagem automática de mensagens com API REST e dashboard interativo em tempo real.

---

## 🧠 O que é este projeto?

Este projeto simula um **sistema de atendimento ao cliente** que recebe mensagens, as **classifica automaticamente por intenção e prioridade** usando regras de IA, armazena os dados em banco SQLite e os exibe em um **dashboard visual e interativo**.

Ideal para aprender como integrar uma API backend com um frontend analítico, ou como base para um sistema real de triagem de suporte.

---

## ✨ Funcionalidades

- 📥 **API REST** para receber mensagens de clientes (`POST /atendimento`)
- 🤖 **Classificação automática** por intenção: `COMPRA`, `PROBLEMA_TECNICO`, `DUVIDA_GERAL`
- 🚨 **Priorização inteligente**: `CRITICA`, `ALTA`, `MEDIA`
- 💬 **Resposta sugerida** gerada automaticamente para cada mensagem
- 🗄️ **Persistência** em banco de dados SQLite local
- 📊 **Dashboard interativo** com atualização a cada 10 segundos
- 🧪 **Script de teste** para popular o banco com dados de exemplo

---

## 🖥️ Demonstração do Dashboard

O dashboard exibe em tempo real:

| Componente | Descrição |
|---|---|
| 📋 KPIs | Total de atendimentos, críticos, alta prioridade e clientes únicos |
| 📈 Gráfico de linha | Atendimentos por dia |
| 🍩 Donut | Distribuição por intenção |
| 📊 Barras | Distribuição por prioridade |
| 🔥 Heatmap | Intenção × Prioridade |
| 📋 Tabela | Últimos 15 registros com destaque por prioridade |

---

## 🗂️ Estrutura do Projeto

```
📁 projeto/
├── main.py           # API FastAPI — endpoints HTTP
├── ia.py             # Lógica de classificação de mensagens
├── database.py       # Camada de acesso ao banco de dados
├── dashboard.py      # Dashboard Dash/Plotly
├── popular_banco.py  # Script para inserir dados de teste
├── requirements.txt  # Dependências do projeto
└── atendimento.db    # Banco SQLite (gerado automaticamente)
```

---

## 🚀 Como rodar o projeto

### Pré-requisitos

- Python **3.10+** instalado
- `pip` disponível no terminal

---

### 1. Clone o repositório

```bash
git clone https://github.com/carlos-lorim/API-leitura-de-mensagens-e-dashboard.git
cd API-leitura-de-mensagens-e-dashboard
```

### 2. (Opcional) Crie um ambiente virtual

```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Inicie a API

> Em um terminal, rode:

```bash
python main.py
```

A API estará disponível em: **http://127.0.0.1:8000**

Documentação interativa (Swagger): **http://127.0.0.1:8000/docs**

---

### 5. Popule o banco com dados de teste

> Em outro terminal (com a API rodando), execute:

```bash
python popular_banco.py
```

Isso envia 12 mensagens de teste para a API e exibe o resultado no terminal:

```
[CRITICA  ] PROBLEMA_TECNICO     <- o sistema nao funciona
[ALTA     ] COMPRA               <- qual o preco do produto?
[MEDIA    ] DUVIDA_GERAL         <- como funciona o periodo de teste?
...
```

---

### 6. Abra o Dashboard

> Em outro terminal, rode:

```bash
python dashboard.py
```

Acesse no navegador: **http://127.0.0.1:8050**

---

## 🔌 Endpoints da API

### `POST /atendimento`

Recebe uma mensagem e retorna a classificação.

**Body:**
```json
{
  "cliente_id": "cliente_01",
  "texto": "o sistema não está funcionando"
}
```

**Resposta:**
```json
{
  "id": 1,
  "timestamp": "2025-04-13 10:30:00",
  "cliente": "cliente_01",
  "mensagem": "o sistema não está funcionando",
  "intencao": "PROBLEMA_TECNICO",
  "prioridade": "CRITICA",
  "resposta_sugerida": "Recebemos sua mensagem sobre PROBLEMA_TECNICO. Um atendente já vai falar com você!"
}
```

---

### `GET /atendimentos?limit=50`

Retorna os últimos N atendimentos registrados.

---

## 🧩 Como funciona a classificação (ia.py)

O módulo `ia.py` analisa o texto da mensagem procurando palavras-chave:

| Palavras-chave | Intenção | Prioridade |
|---|---|---|
| preço, comprar, valor, custo, orçamento... | `COMPRA` | `ALTA` |
| erro, problema, não funciona, bug, falha... | `PROBLEMA_TECNICO` | `CRITICA` |
| *(qualquer outro texto)* | `DUVIDA_GERAL` | `MEDIA` |

> A arquitetura foi pensada para facilitar a substituição desta lógica por um modelo de NLP ou LLM real no futuro.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | API REST |
| [Uvicorn](https://www.uvicorn.org/) | Servidor ASGI |
| [Pydantic](https://docs.pydantic.dev/) | Validação de dados |
| [SQLite](https://www.sqlite.org/) | Banco de dados local |
| [Pandas](https://pandas.pydata.org/) | Manipulação de dados |
| [Dash](https://dash.plotly.com/) | Dashboard web |
| [Plotly](https://plotly.com/) | Gráficos interativos |

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e distribuir.

---

<p align="center">Feito com 🐍 Python por <a href="https://github.com/carlos-lorim">carlos-lorim</a></p>
