# DATATHON STREAMLIT APP | PÓS TECH

![Status](https://img.shields.io/badge/STATUS-CONCLUÍDO-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)
![Deploy](https://img.shields.io/badge/DEPLOY-Streamlit_Cloud-orange)

## 📋 Índice
- [Introdução](#-introdução)
- [Objetivo](#🎯-objetivo)
- [Funcionalidades](#✨-funcionalidades)
- [Tecnologias](#🛠-tecnologias)
- [Organização do Projeto](#📁-organização-do-projeto)
- [Instalação e Uso](#🚀-instalação-e-uso)
- [Estrutura da Aplicação](#🏗-estrutura-da-aplicação)

## 🏁 Introdução

Esta aplicação Streamlit foi desenvolvida como parte do **Datathon da Pós Tech**, servindo como interface frontend para o sistema completo de recrutamento e seleção inteligente.

A aplicação consome a API backend que incorpora técnicas avançadas de RAG (Retrieval-Augmented Generation) e processamento de linguagem natural, proporcionando uma experiência intuitiva para recrutadores e gestores de RH.

Através de uma interface amigável, usuários podem gerenciar vagas, buscar candidatos de forma inteligente e obter análises detalhadas de compatibilidade entre perfis e oportunidades.

## 🎯 Objetivo

Fornecer uma interface web moderna e acessível para:
- **Gestão visual de vagas** com operações CRUD completas
- **Busca semântica intuitiva** em bancos de dados de currículos
- **Visualização clara** de resultados e análises
- **Processamento simplificado** de documentos e candidaturas
- **Dashboard interativo** com métricas e insights

## ✨ Funcionalidades

### 📊 Dashboard Principal
- Visão geral do sistema de recrutamento
- Métricas de vagas ativas e candidatos
- Acesso rápido às funcionalidades principais

### 👥 Gestão Visual de Vagas
- Criação de novas vagas com formulários intuitivos
- Listagem e filtragem de vagas existentes
- Edição e exclusão com confirmação visual
- Visualização detalhada de cada vaga

### 🔍 Busca Inteligente
- Interface unificada para busca híbrida
- Configuração de parâmetros de busca
- Visualização organizada dos resultados
- Detalhes completos dos candidatos encontrados

### 🤖 Análise com IA
- Formulário para análise de compatibilidade
- Configuração de parâmetros do modelo LLM
- Exibição formatada das análises geradas
- Histórico de consultas realizadas

## 🛠 Tecnologias

### Frontend & UI
- **Streamlit** - Framework principal para interface web
- **Pandas** - Manipulação e exibição de dados tabulares

### Integração & Comunicação
- **Requests** - Comunicação HTTP com a API backend
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

### Deploy & Infraestrutura
- **Streamlit Community Cloud** - Hospedagem e deploy
- **GitHub Integration** - Deploy contínuo via repositório

## 📁 Organização do Projeto
```
datathon_agent_rag/
├── frontend/ # Módulos da interface Streamlit
│ ├── st_crud.py # Gestão de vagas (CRUD)
│ ├── st_search.py # Busca semântica
│ ├── st_llm.py # Análise com IA
│ ├── st_select.py # Seleção de vagas
│ ├── st_summary.py # Resumo das vagas
│ └── st_upload.py # Upload de currículos
├── pipeline/ # Processamento de dados
│ ├── create_collection.py # Criação de collections
│ ├── ingestion.py # Ingestão de dados
│ └── schema_metadata.py # Schemas e metadados
├── config/ # Configurações do sistema
│ └── clients.py # Clients para serviços externos
├── app.py # Aplicação principal Streamlit
├── requirements.txt # Dependências do projeto
├── .env # Variáveis de ambiente
└── README.md # Documentação
```

## 💻 Acesso à Aplicação

**Aplicação Deployada:** https://datathonagentrag-agent-ai.streamlit.app/

## 🚀 Instalação e Uso

### Pré-requisitos
- Python 3.8+
- Conexão com a API backend
- Acesso à internet para modelos externos

### 📥 Instalação Local

1. **Clone o repositório**
```bash
git clone https://github.com/cezarmaldini/datathon_agent_rag.git
cd datathon_agent_rag
```

2. **Crie um ambiente virtual**
```
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```
pip install -r requirements.txt
````

4. **Configure as variáveis de ambiente**
```
# Edite o arquivo .env
API_BASE_URL=https://sua-api.aplicacao.com
OPENAI_API_KEY=sua-chave-openai
QDRANT_URL=sua-url-qdrant
QDRANT_API_KEY=sua-chave-qdrant
```

5. **Execute a aplicação**
```
streamlit run app.py
```

## 🏗️ Estrutura da Aplicação

### Aplicação Principal (`app.py`)
- **Configuração** da página Streamlit
- **Navegação** entre módulos via sidebar
- **Gestão de estado** entre páginas
- **Inicialização** de componentes globais

### Módulo CRUD (`frontend/st_crud.py`)
- **Operações completas** de banco de dados
- **Formulários dinâmicos** com validação
- **Tabelas interativas** para listagem
- **Gestão de estado** das vagas selecionadas

### Módulo de Busca (`frontend/st_search.py`)
- **Interface de busca** unificada
- **Parâmetros configuráveis** de pesquisa
- **Resultados em tempo real**
- **Exportação** de dados encontrados

### Módulo LLM (`frontend/st_llm.py`)
- **Integração com OpenAI** e outros modelos
- **Análise contextual** de candidaturas
- **Geração de insights** automáticos
- **Histórico** de consultas realizadas

### Pipeline de Dados (`pipeline/`)
- **Processamento** de documentos
- **Geração de embeddings**
- **Gestão de collections** no vector store
- **Validação** de schemas de dados

## 👥 Autor
- Cezar Maldini

- GitHub: @cezarmaldini

- Projeto: [Datathon Pós Tech]

---

⭐️ Se este projeto foi útil, considere dar uma estrela no repositório!