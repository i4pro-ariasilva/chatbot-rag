# Chatbot RAG# Chatbot RAG Ultra-Otimizado 🚀# 🤖 Chatbot RAG Ultra-Otimizado



Sistema de chatbot com Retrieval-Augmented Generation (RAG) otimizado para consultas rápidas em documentos internos.



## CaracterísticasSistema de chatbot com Retrieval-Augmented Generation (RAG) ultra-otimizado para resposta rápida e eficiente sobre documentos internos.Sistema inteligente de chatbot que combina **Retrieval-Augmented Generation (RAG)** para responder perguntas sobre documentação interna com **performance otimizada**.



- **Performance Otimizada**: Inicialização rápida com sistema de cache

- **Interface Web**: Interface moderna e responsiva

- **TF-IDF Avançado**: Algoritmo otimizado para busca eficiente## 🌟 Características## 🎯 Características Principais

- **API RESTful**: Endpoints para integração

- **Monitoramento**: Métricas de performance em tempo real



## Instalação Rápida- **Performance Ultra-Rápida**: Inicialização em ~12s (vs 30s+ anterior)- **� Ultra Performance**: Cache avançado e algoritmos otimizados



### Pré-requisitos- **Sistema de Cache Multi-Camadas**: Cache LRU, cache de respostas e cache de similaridade- **📄 Processamento Inteligente**: Suporte a HTML e texto com chunking otimizado

- Python 3.8+

- Conta Groq (gratuita em [console.groq.com](https://console.groq.com/))- **TF-IDF Otimizado**: Valores pré-computados e early stopping- **� RAG Avançado**: TF-IDF otimizado + Groq API para respostas precisas



### Passos de Instalação- **Interface Moderna**: UI responsiva e intuitiva- **🌐 Interface Moderna**: Interface web responsiva com métricas de performance



1. **Clone o repositório**- **Monitoramento**: Métricas de performance em tempo real- **� Cache Inteligente**: Sistema de cache multi-camadas para velocidade máxima

```bash

git clone https://github.com/i4pro-ariasilva/chatbot-rag.git- **⚡ Inicialização Rápida**: Sistema pronto em segundos

cd chatbot-rag

```## 🚀 Início Rápido



2. **Instale as dependências**## 🏗️ Arquitetura

```bash

pip install -r requirements.txt### Pré-requisitos

```

- Python 3.8+```

3. **Configure o ambiente**

```bash- Chave da API Groq (gratuita em [console.groq.com](https://console.groq.com/))chatbot_rag/

cp .env.example .env

# Edite o arquivo .env e adicione sua chave da API Groq├── backend/

```

### Instalação│   ├── main.py              # Servidor FastAPI otimizado

4. **Adicione seus documentos**

- Coloque arquivos .txt na pasta `db_intern/`│   ├── document_processor.py # Processamento de documentos



5. **Execute o sistema**1. **Clone o repositório**│   └── rag_engine.py        # RAG engine ultra-otimizado

```bash

# Windows```bash├── frontend/

start.bat

git clone <url-do-seu-repo>│   └── index.html           # Interface web moderna

# Linux/Mac

python backend/main.pycd chatbot_rag├── config/

```

```│   └── settings.py          # Configurações

6. **Acesse o chatbot**

- Abra seu navegador em: http://localhost:8000├── db_intern/              # Documentos da base de conhecimento



## Estrutura do Projeto2. **Instale as dependências**├── vector_db/              # Banco de dados SQLite



``````bash├── cache/                  # Cache de performance

chatbot-rag/

│pip install -r requirements.txt├── .env                    # Variáveis de ambiente

├── backend/                 # Código do servidor

│   ├── main.py             # Servidor FastAPI```├── requirements.txt        # Dependências Python

│   ├── rag_engine.py       # Engine de busca otimizada

│   └── document_processor.py # Processamento de documentos├── start.bat              # Script de inicialização

│

├── frontend/                # Interface web3. **Configure o ambiente**└── README.md              # Esta documentação

│   ├── index.html          # Página principal

│   └── img/                # Recursos visuais```bash```

│

├── config/                  # Configurações# Copie o arquivo de exemplo

│   └── settings.py         # Configurações do sistema

│copy .env.example .env## 🚀 Início Rápido

├── docs_exemplo/            # Documentos de exemplo

│   ├── exemplo_documento.txt# Edite o .env e adicione sua chave da API Groq

│   └── documentacao_api.txt

│```### Pré-requisitos

├── .env.example            # Template de configuração

├── .gitignore              # Arquivos ignorados pelo Git- Python 3.8+ 

├── requirements.txt        # Dependências Python

├── start.bat              # Script de inicialização (Windows)4. **Adicione seus documentos**- Conexão com internet (para API Groq, opcional)

└── README.md              # Esta documentação

```- Coloque seus arquivos .txt na pasta `db_intern/`



## Configuração### 1. Inicialização Automática



### Arquivo .env5. **Execute o sistema**```bash



Copie o arquivo `.env.example` para `.env` e configure:```bash# Execute o script de inicialização



```env# Windowsstart.bat

# Diretório dos documentos

DOCUMENTS_DIR=./db_internstart.bat```



# API Groq (obrigatório)# Ou manualmente

GROQ_API_KEY=sua_chave_aqui

API_PROVIDER=groqpython backend/main.py### 2. Inicialização Manual

GROQ_MODEL=llama-3.1-8b-instant

`````````bash



### Obtendo Chave da API Groq# Instale as dependências



1. Acesse [console.groq.com](https://console.groq.com/)6. **Acesse o chatbot**pip install -r requirements.txt

2. Crie uma conta gratuita

3. Vá em "API Keys"```

4. Gere uma nova chave

5. Cole a chave no arquivo `.env`http://localhost:8000# Inicie o servidor



## Uso```python backend/main.py



### Interface Web```

1. Acesse http://localhost:8000

2. Digite sua pergunta## 📁 Estrutura do Projeto

3. Pressione Enter ou clique "Enviar"

4. Aguarde a resposta baseada nos documentos### 3. Acesse a Interface



### API```Abra seu navegador em: `http://localhost:8000`



**Endpoint de Chat**chatbot_rag/

```bash

POST /chat├── backend/             # Código do servidor## ⚙️ Configuração

Content-Type: application/json

├── frontend/            # Interface web

{

  "message": "sua pergunta aqui"├── config/              # Configurações### Variáveis de Ambiente (.env)

}

```├── db_intern/           # Seus documentos (.txt)```env



**Status do Sistema**├── requirements.txt     # Dependências Python# API Groq (opcional, mas recomendado)

```bash

GET /status├── start.bat           # Script de inicializaçãoGROQ_API_KEY=sua_chave_aqui

```

├── .env.example        # Exemplo de configuraçãoGROQ_MODEL=llama3-8b-8192

## Performance

└── README.md           # Este arquivo

- **Inicialização**: ~12 segundos para 1000+ documentos

- **Primeira consulta**: ~9 segundos```# Configurações do sistema

- **Consultas subsequentes**: 2-5 segundos (com cache)

- **Capacidade testada**: 1.120 documentos, 9.500+ chunksDOCUMENTS_DIR=db_intern



## Solução de Problemas## ⚙️ ConfiguraçãoVECTOR_DB_PATH=vector_db/documents.db



### Erro de inicializaçãoCOLLECTION_NAME=i4pro_docs

```bash

# Verifique dependências### Arquivo .env (obrigatório)```

pip install -r requirements.txt

```env

# Verifique arquivo .env

cat .envDOCUMENTS_DIR=./db_intern### Adicionando Documentos

```

GROQ_API_KEY=sua_chave_groq_aqui1. Coloque seus arquivos `.txt` ou `.html` no diretório `db_intern/`

### Performance lenta

- Verifique se o cache está habilitadoAPI_PROVIDER=groq2. Reinicie o servidor para indexar os novos documentos

- Acesse `/status` para métricas

- Verifique logs no terminalGROQ_MODEL=llama-3.1-8b-instant



### Problemas com documentos```## 🎛️ Uso da Interface

- Use apenas arquivos .txt

- Verifique caminho em `DOCUMENTS_DIR`

- Confirme que existem documentos em `db_intern/`

### Obtendo a Chave da API Groq1. **Status do Sistema**: Mostra se o sistema está pronto e quantos documentos foram indexados

## Contribuição

1. Acesse [console.groq.com](https://console.groq.com/)2. **Chat Interativo**: Digite perguntas e receba respostas baseadas na documentação

1. Fork o projeto

2. Crie uma branch: `git checkout -b minha-feature`2. Crie uma conta gratuita3. **Métricas de Performance**: Tempo de resposta e fontes consultadas

3. Commit: `git commit -m 'Adiciona nova feature'`

4. Push: `git push origin minha-feature`3. Gere uma API key4. **Limpeza de Cache**: Botão para otimizar a memória quando necessário

5. Abra um Pull Request

4. Adicione no arquivo `.env`

## Licença

## 📊 Performance

Este projeto está sob a licença MIT.

## 📊 Performance

## Suporte

- **Inicialização**: ~10-15 segundos para 1000+ documentos

- Documentação: Este README

- Issues: [GitHub Issues](https://github.com/i4pro-ariasilva/chatbot-rag/issues)- **Inicialização**: ~12 segundos para 1.000+ documentos- **Resposta**: < 1 segundo para consultas em cache

- Exemplos: Pasta `docs_exemplo/`
- **Primeira consulta**: ~9 segundos- **Resposta**: 2-5 segundos para consultas novas

- **Consultas subsequentes**: 2-5 segundos (com cache)- **Cache Hit Rate**: 70-80% em uso normal

- **Capacidade**: Testado com 1.120 documentos e 9.500+ chunks- **Índices**: Criados automaticamente para máxima velocidade



## 🔍 Solução de Problemas## 🔧 Recursos Técnicos



### Erro de inicialização### Cache Multi-Camadas

```bash- **Cache TF-IDF**: Modelo persistente entre reinicializações

pip install -r requirements.txt- **Cache de Consultas**: Respostas similares servidas instantaneamente

# Verifique se o .env existe e tem a chave da API- **Cache de Similaridade**: Cálculos de relevância otimizados

```

### Algoritmos Otimizados

### Performance lenta- **TF-IDF Avançado**: Com pré-computação de valores IDF

- Verifique se o cache está habilitado- **Chunking Inteligente**: Breakpoints baseados em conteúdo

- Acesse `/status` para métricas em tempo real- **Busca Eficiente**: Early stopping e índices em memória



## 🤝 Contribuição### API Endpoints

- `GET /` - Interface web

1. Fork o projeto- `POST /chat` - Envio de perguntas

2. Crie uma branch (`git checkout -b feature/AmazingFeature`)- `GET /status` - Status do sistema

3. Commit suas mudanças (`git commit -m 'Add AmazingFeature'`)- `GET /health` - Health check

4. Push (`git push origin feature/AmazingFeature`)- `POST /clear-cache` - Limpeza de cache

5. Abra um Pull Request

## 🛠️ Solução de Problemas

---

### Servidor não inicia

**Desenvolvido com ❤️ para máxima performance e facilidade de uso**```bash
# Verifique as dependências
pip install -r requirements.txt

# Verifique a porta 8000
netstat -an | findstr :8000
```

### Performance lenta
```bash
# Limpe o cache via interface ou API
curl -X POST http://localhost:8000/clear-cache
```

### Erro de API Groq
- Verifique a chave API no arquivo `.env`
- O sistema funciona sem API (modo fallback)

## 📝 Desenvolvimento

### Estrutura de Código
- **FastAPI**: Framework web assíncrono
- **SQLite**: Banco de dados leve e rápido
- **TF-IDF**: Algoritmo de relevância otimizado
- **LRU Cache**: Cache inteligente em memória
- **Groq API**: LLM para geração de respostas

### Logs
Logs detalhados estão disponíveis no console para debugging e monitoramento de performance.

---

**Versão**: 3.0 Ultra-Otimizada  
**Compatibilidade**: Python 3.8+  
**Licença**: Uso Interno
pip install -r requirements.txt
```

### 2. Preparar Documentos

Coloque seus arquivos HTML na pasta `db_intern`:

```
C:\Users\ariasilva\Documents\COPILOT\Semana_03\chatbot_rag\db_intern\
├── processo-desenvolvimento.html
├── arquitetura-sistema.html
├── manual-api.html
└── ...outros documentos HTML
```

## 🎮 Como Usar

### Método Automático (Recomendado)

```powershell
# Navegue até o diretório
cd "C:\Users\ariasilva\Documents\COPILOT\Semana_03\chatbot_rag"

# Execute o script de setup
.\setup.bat

# Execute o script de início
.\start.bat
```

### 3. Acessar a Interface

Abra seu navegador e acesse: **http://localhost:8000**

O sistema irá:
1. Escanear automaticamente o diretório `db_intern`
2. Processar arquivos HTML (apenas texto)
3. Criar vetores TF-IDF e armazenar no SQLite
4. Ficar pronto para responder perguntas!

## 📊 API Endpoints

- `GET /` - Interface web principal
- `GET /health` - Status de saúde do sistema
- `GET /status` - Informações detalhadas do sistema
- `POST /chat` - Endpoint principal do chat
- `POST /reindex` - Re-indexar documentos
- `GET /documents` - Listar documentos processados
- `GET /docs` - Documentação automática da API

## 💡 Exemplos de Perguntas

- "Como é o processo de deploy da aplicação?"
- "Quais são as etapas de desenvolvimento de uma nova feature?"
- "Como funciona a arquitetura do sistema de seguros?"
- "Quais são os padrões de código que devemos seguir?"
- "Como fazer a configuração do ambiente de desenvolvimento?"

## ⚙️ Configurações Avançadas

### Alterar Modelo de IA

Para usar um modelo diferente, altere no arquivo `.env`:

```env
# Opções disponíveis:
OLLAMA_MODEL=codellama:13b-instruct  # Melhor para código
OLLAMA_MODEL=mistral:7b-instruct     # Mais rápido, menos recursos
OLLAMA_MODEL=llama2:13b-chat         # Conversação geral
```

### Ajustar Chunking

No arquivo `.env`, você pode ajustar como os documentos são divididos:

```env
CHUNK_SIZE=1000          # Tamanho dos chunks de texto
CHUNK_OVERLAP=200        # Sobreposição entre chunks
MAX_CONTEXT_LENGTH=4000  # Contexto máximo enviado para IA
```

## 🔧 Troubleshooting

### Problemas Comuns

**1. "Ollama connection failed"**
- Verifique se o Ollama está rodando: `ollama serve`
- Confirme se o modelo foi baixado: `ollama list`

**2. "Documents directory not found"**
- Verifique se a pasta `db_intern` existe
- Coloque seus documentos HTML e imagens nesta pasta

**3. "Import errors" durante instalação**
- Execute `.\setup.bat` que configura tudo automaticamente
- Ou instale manualmente: `pip install -r requirements.txt --force-reinstall`

**4. OCR não funciona**
- Instale o Tesseract OCR
- No Windows, adicione o Tesseract ao PATH

### Logs e Debug

O sistema gera logs detalhados no console. Para mais informações, inicie com:

```powershell
cd backend
python main.py
```

## 🤝 Contribuição

Este é um projeto interno da empresa. Para melhorias ou bugs:

1. Documente o problema detalhadamente
2. Inclua logs relevantes
3. Sugira melhorias específicas
4. Teste em ambiente de desenvolvimento

## 📝 Licença

Uso interno da empresa. Todos os direitos reservados.

---

## 🚀 Quick Start

```powershell
# 1. Instalar Ollama e baixar modelo
ollama serve
ollama pull codellama:13b-instruct

# 2. Navegar até o projeto
cd "C:\Users\ariasilva\Documents\COPILOT\Semana_03\chatbot_rag"

# 3. Executar setup
.\setup.bat

# 4. Colocar documentos na pasta db_intern

# 5. Iniciar sistema
.\start.bat

# 6. Acessar: http://localhost:8000
```

**Pronto! Seu chatbot RAG está funcionando! 🎉**