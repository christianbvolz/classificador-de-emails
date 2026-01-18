# Classificador de Email

**Visão Geral:**
- **Contexto:** Este repositório contém uma solução para classificar emails em **Produtivo** ou **Improdutivo** e gerar respostas automáticas, conforme descrito em [contextoDesafio.md](contextoDesafio.md).

## �️ Estrutura do Projeto

```
classificador-de-email/
├── backend/                    # API FastAPI + IA
│   ├── app/                   # Código da aplicação
│   │   ├── main.py           # Endpoints da API
│   │   ├── services.py       # Integração com LLM
│   │   ├── utils.py          # Pipeline NLP
│   │   ├── schemas.py        # Modelos Pydantic
│   │   ├── templates.py      # Templates de respostas
│   │   └── exceptions.py     # Tratamento de erros
│   ├── Dockerfile            # Container backend
│   ├── requirements.txt      # Dependências Python
│   └── .env                  # Variáveis de ambiente
├── frontend/                  # Interface web React + TypeScript
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   ├── utils/            # Utilitários
│   │   ├── App.tsx           # Componente principal
│   │   ├── api.ts            # Cliente da API
│   │   └── types.ts          # Tipos TypeScript
│   ├── Dockerfile            # Container frontend (Nginx)
│   ├── package.json          # Dependências Node
│   └── .env.local            # Variáveis de ambiente
├── docker-compose.yml         # Orquestração full stack
└── README.md                  # Este arquivo
```

## 🌐 Aplicação em Produção

### Frontend (Interface Web)
**URL:** https://classificador-de-emails-mauve.vercel.app/

**Funcionalidades:**
- ✍️ Input manual de emails (assunto + corpo)
- 📁 Upload de arquivos (.txt com múltiplos emails)
- 🎨 Interface moderna com React + TypeScript + TailwindCSS
- 📋 Resultados com classificação, categoria e respostas sugeridas
- 📝 Copiar assunto, corpo ou resposta completa

### API (Backend)
**URL Base:** https://classificador-de-emails-qts5.onrender.com

**Endpoints Disponíveis:**
- 📖 **Documentação Interativa:** https://classificador-de-emails-qts5.onrender.com/docs
- ❤️ **Health Check:** https://classificador-de-emails-qts5.onrender.com/health
- 📧 **Processar Emails:** `POST https://classificador-de-emails-qts5.onrender.com/process-email`

**Monitoramento:**
- 🟢 API monitorada 24/7 via [UptimeRobot](https://uptimerobot.com)
- ⏱️ Verificações a cada 5 minutos
- 🔄 Uptime garantido (sem sleep mode)

---

## Funcionalidades Implementadas

### **Backend API (FastAPI)**
- **Endpoint principal:** `POST /process-email` em [backend/app/main.py](backend/app/main.py)
- **Processamento em lote:** Aceita 1-10 emails por requisição através do modelo [EmailListRequest](backend/app/schemas.py)
- **Validação robusta:** Usa Pydantic com `conlist` para garantir limites de batch (min: 1, max: 10)
- **Tratamento de exceções:** Handler customizado para [AppError](backend/app/exceptions.py) com códigos de erro específicos
- **Documentação interativa:** Swagger UI disponível em `/docs` com exemplos de uso

### **Sistema de Templates de Respostas** ([app/templates.py](app/templates.py))
- **6 categorias de email suportadas:**
  - `payment_issue`: Problemas de pagamento, cobranças, faturas
  - `technical_support`: Bugs, crashes, erros técnicos
  - `information_request`: Perguntas sobre features, preços, documentação
  - `greeting`: Mensagens casuais, cumprimentos, interações sociais
  - `complaint`: Insatisfação, feedback negativo, reclamações
  - `spam`: Conteúdo promocional, mensagens irrelevantes
- **Templates bilíngues (PT/EN)** com respostas profissionais para cada categoria
- **Metadata por categoria:** Descrições e exemplos para prompt engineering
- **Funções auxiliares:** `get_template()`, `get_all_categories()`, `get_category_description()`

### **Pipeline de Processamento de Emails**
1. **Limpeza de texto** ([app/utils.py](app/utils.py)):
   - Remoção de HTML tags, URLs e endereços de email via regex
   - Detecção automática de idioma com `langdetect` (suporte a PT e EN)
   - Lematização contextual usando spaCy quando modelo está disponível
   - Remoção de stop words, pontuação e espaços desnecessários
   - Cache LRU para modelos spaCy (otimiza performance)

2. **Classificação inteligente via LLM** ([app/services.py](app/services.py)):
   - Modelo: **Llama-3.3-70b-versatile** via API Groq
   - Classificação binária: produtivo (requer ação) vs. improdutivo
   - **Identificação automática de categoria** entre as 6 categorias disponíveis
   - Geração de respostas personalizadas baseadas na categoria identificada
   - Sistema de fallback inteligente com templates específicos por categoria

### **Schemas e Validação** ([app/schemas.py](app/schemas.py))
- **EmailRequest:** Modelo para email individual (subject + body)
- **EmailListRequest:** Batch de 1-10 emails com validação automática
- **EmailResponse:** Resposta com:
  - `isProductive` (camelCase via alias_generator)
  - `suggestedSubject` e `suggestedBody`
  - `detectedLanguage`
  - `originalEmail` (para referência)
- Documentação automática de exemplos no schema JSON

### **Tratamento de Erros** ([app/exceptions.py](app/exceptions.py))
- **AppError:** Classe base com status_code e message
- **NLPProcessingError:** Para falhas no pipeline de NLP
- **LLMServiceError:** Para falhas na API Groq
- Logging estruturado para monitoramento e debugging

### **Deploy e Infraestrutura**
- **Dockerfile:** Imagem otimizada com Python 3.11 + dependências
- **docker-compose.yml:** Orquestração simplificada com mapeamento de portas
- **Variáveis de ambiente:** `.env` para configuração de API keys
- **Modelos spaCy:** Pré-instalados no container (pt_core_news_sm, en_core_web_sm)

**O que NÃO foi implementado / pendente:**
- Persistência de dados (banco de dados)
- Testes automatizados (unitários e integração)
- Pipeline CI/CD
- Rate limiting e autenticação na API
- Sistema de feedback para melhorar classificações

## Como Rodar

### **Opção 1: Docker Compose (Recomendado - Full Stack)**

1. **Clone o repositório:**
   ```bash
   git clone git@github.com:christianbvolz/classificador-de-emails.git
   cd classificador-de-emails
   ```

2. **Configure as variáveis de ambiente:**
   
   **Backend** (`backend/.env`):
   ```bash
   GROQ_API_KEY=seu_token_aqui
   ```
   > Obtenha sua chave em: https://console.groq.com/keys
   
   **Frontend** (`frontend/.env.local`):
   ```bash
   VITE_API_URL=http://localhost:8000
   ```

3. **Inicie os containers:**
   ```bash
   docker compose up --build
   ```

4. **Acesse a aplicação:**
   - **Frontend:** http://localhost:3000
   - **API (Swagger):** http://localhost:8000/docs
   - **API (Endpoint):** http://localhost:8000/process-email

### **Opção 2: Instalação Local (Desenvolvimento)**

**Backend:**
1. **Instale dependências:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   python -m spacy download pt_core_news_sm
   ```

2. **Configure `backend/.env`:**
   ```bash
   GROQ_API_KEY=seu_token_aqui
   ```

3. **Inicie o servidor:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

**Frontend:**
1. **Instale dependências:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure `frontend/.env.local`:**
   ```bash
   VITE_API_URL=http://localhost:8000
   ```

3. **Inicie o dev server:**
   ```bash
   npm run dev
   ```
   Acesse: http://localhost:5173

### **Exemplos de Uso**

**Exemplo 1: Email único (produtivo)**
```bash
curl -X POST "http://localhost:8000/process-email" \
  -H "Content-Type: application/json" \
  -d '{
    "emails": [
      {
        "subject": "Problema com pagamento",
        "body": "Olá, não consigo processar o pagamento da minha fatura. Preciso de ajuda urgente."
      }
    ]
  }'
```

**Exemplo 2: Batch de emails (mix produtivo/improdutivo)**
```bash
curl -X POST "http://localhost:8000/process-email" \
  -H "Content-Type: application/json" \
  -d '{
    "emails": [
      {
        "subject": "Technical Issue",
        "body": "The app crashes when I try to export data."
      },
      {
        "subject": "Happy Holidays",
        "body": "Just wanted to wish you a great Christmas!"
      }
    ]
  }'
```

**Resposta esperada:**
```json
[
  {
    "isProductive": true,
    "category": "payment_issue",
    "suggestedSubject": "Re: Problema com Pagamento - Equipe Financeira",
    "suggestedBody": "Prezado(a) cliente,\n\nRecebemos sua solicitação referente ao problema com pagamento...",
    "detectedLanguage": "pt",
    "originalEmail": "Subject: Problema com pagamento\n\nBody: Olá, não consigo..."
  }
]
```

---

## Arquitetura Técnica

### **Stack Tecnológico**

**Backend:**
- **Framework:** FastAPI 0.115+ (async, high-performance)
- **LLM Provider:** Groq Cloud API (Llama-3.3-70b-versatile)
- **NLP:** spaCy 3.8+ com modelos pt_core_news_sm e en_core_web_sm
- **Validação:** Pydantic v2 com alias_generator e conlist
- **Language Detection:** langdetect (baseado em n-grams)
- **Templates:** Sistema modular de templates bilíngues (6 categorias)

**Frontend:**
- **Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **Styling:** TailwindCSS v3
- **Icons:** Lucide React
- **HTTP Client:** Fetch API nativa

**Infraestrutura:**
- **Containers:** Docker + Docker Compose
- **Backend Deploy:** Render (monitorado por UptimeRobot)
- **Frontend Deploy:** Vercel (CDN global, zero downtime)
- **Network:** Bridge network para comunicação entre containers

### **Fluxo de Processamento**
```
1. Cliente → POST /process-email (batch de 1-10 emails)
2. FastAPI → Validação com Pydantic (EmailListRequest)
3. Para cada email:
   a. Combina subject + body
   b. utils.clean_email_text() → regex + langdetect + spaCy lemmatization
   c. services.classify_and_respond():
      - Carrega descrições e exemplos de todas as categorias
      - Constrói prompt com few-shot learning usando templates
      - Groq API (Llama-3.3) → classifica e gera resposta
   d. Validação de resposta (incluindo categoria) → fallback se necessário
4. Retorna List[EmailResponse] com classificação, categoria e respostas sugeridas
```

### **Otimizações Implementadas**
- **Cache de modelos:** `@lru_cache` para spaCy (evita reloads)
- **Processamento em lote:** Aceita até 10 emails por request
- **Fallback inteligente:** Templates pré-definidos quando LLM falha
- **Logging estruturado:** Monitora tokens, idioma e classificações
- **JSON mode:** `response_format={"type": "json_object"}` no Groq para parsing confiável
- **Prompt otimizado para tokens:**
  - Envia apenas exemplos do idioma detectado (reduz ~50% dos tokens)
  - Usa apenas 3 exemplos representativos ao invés de 12
  - Descrições de categorias simplificadas
  - Instruções condensadas
  - **Consumo esperado: 400-700 tokens/request** (input + output)

**Observações técnicas importantes:**
- O código atualmente chama a API Groq (`groq` client). Garanta que `GROQ_API_KEY` esteja configurada. Obtenha sua chave em https://console.groq.com/keys
- A pipeline de NLP tenta carregar modelos spaCy; se o modelo não existir, há um fallback simples de limpeza de texto
- A resposta do LLM é esperada em JSON estrito contendo `is_productive`, `category`, `suggested_subject` e `suggested_body`
- Cada email no batch é processado sequencialmente para controle de rate limits
- CamelCase automático nas respostas JSON via `alias_generator=to_camel`
- Templates organizados em arquivo separado ([app/templates.py](app/templates.py)) para fácil manutenção e expansão

---


## Técnicas de Prompt Engineering Aplicadas

Para maximizar a qualidade das respostas geradas pela IA, foram aplicadas as seguintes técnicas de engenharia de prompt:

### 1. **Few-Shot Learning com Templates Dinâmicos**
- Exemplos de classificação e resposta são gerados automaticamente a partir de `RESPONSE_TEMPLATES` em [templates.py](app/templates.py)
- Fornece à IA padrões concretos para **6 categorias distintas** em português e inglês
- Cada categoria tem templates profissionais específicos:
  - `payment_issue`: Resposta da equipe financeira com SLA de 24h
  - `technical_support`: Resposta da equipe de engenharia
  - `information_request`: Resposta informativa do atendimento
  - `greeting`: Resposta cordial e breve
  - `complaint`: Resposta empática com escalação para gerência
  - `spam`: Resposta mínima
- Mantém consistência: templates usados como exemplos são os mesmos usados como fallback
- Estrutura de exemplos inclui output JSON completo: `is_productive`, `category`, `suggested_subject`, `suggested_body`

### 2. **Estrutura de Contexto Hierárquica**
O prompt segue um fluxo lógico de raciocínio dividido em seções:

**AVAILABLE CATEGORIES:**
- Lista todas as 6 categorias com descrições detalhadas e exemplos de cada uma
- Ajuda o LLM a entender claramente os limites entre categorias

**CONTEXT FOR THE RESPONSE:**
1. **Category identification** — identifica primeiro a categoria do email entre as 6 disponíveis
2. **Use of texts** — instrução clara de usar texto limpo para análise e original para personalização
3. **Perspective** — define quem está respondendo baseado na categoria (Financial Team, Technical Team, Customer Service, etc.)
4. **Tone** — estabelece tom ajustado por categoria (mais empático para complaints, mais direto para information_request)
5. **Personalization** — instrui a usar detalhes específicos do email original
6. **Structure** — define organização clara (3 parágrafos: saudação, conteúdo, fechamento)
7. **Length** — limita tamanho (100-250 palavras)

**OUTPUT RULES:**
- Define exatamente o que cada campo deve conter (`is_productive`, `category`, `suggested_subject`, `suggested_body`)
- Especifica critérios claros de classificação:
  - Produtivo (requer ação): payment_issue, technical_support, information_request, complaint
  - Improdutivo (sem ação): greeting, spam
- Campo `category` obrigatório com validação das 6 categorias disponíveis
- Exemplos concretos de output para cada categoria

### 3. **Dual Text Strategy (Processamento Duplo)**
- **Texto limpo** (lematizado): Usado pelo LLM para análise semântica, extração de intenção e classificação
- **Texto original**: Usado para personalização (nomes, números de referência, citações)
- Evita que ruído no texto original afete a classificação, mas preserva detalhes importantes para respostas personalizadas

### 4. **Instruções Claras de Output Estruturado**
- Usa `response_format={"type": "json_object"}` do Groq API para garantir JSON válido
- Define schema explícito: `{is_productive: bool, suggested_subject: str, suggested_body: str}`
- Instruções finais reforçam: "Return strictly JSON with keys: ..."

### 5. **Temperatura Otimizada**
- `temperature=0.3` — equilíbrio entre criatividade e consistência
- Baixa o suficiente para respostas previsíveis e confiáveis
- Alta o suficiente para personalização natural e variação de linguagem

### 6. **Validação e Fallback Robusto**
Implementado em `_validate_response()` e `_get_fallback_response()`:
- Valida campos obrigatórios e tamanho mínimo de conteúdo (>50 chars body, >5 chars subject)
- Em caso de falha de validação ou erro de parsing, usa templates pré-definidos
- Garante que a API sempre retorna uma resposta válida
- Seleciona template baseado em idioma detectado e classificação

### 7. **Limitação de Tokens e Custos**
- `max_tokens=600` — controla custo e previne respostas excessivamente longas (reduzido de 800)
- Combinado com instrução de tamanho no prompt (100-250 palavras)
- **Prompt otimizado:**
  - Only few-shot examples for detected language (PT ou EN, não ambos)
  - 3 exemplos representativos ao invés de 12 (payment_issue, technical_support, greeting)
  - Descrições simplificadas de categorias (inline ao invés de estrutura detalhada)
  - Instruções condensadas (7 linhas vs. 20+ anteriormente)
- **Redução de ~60% no consumo de tokens de input**
- Equilibra qualidade vs. custo operacional

### 8. **Privacy-Aware Redaction**
- Instrução no prompt para aplicar redação sensível quando necessário
- Mantém personalização sem expor dados sensíveis desnecessariamente
- Balanceamento entre personalização e privacidade

---

## Próximos Passos

### **Melhorias de Produto**
- [ ] Dashboard de analytics (volume de emails, taxa produtivo/improdutivo, idiomas)

### **Melhorias Técnicas**
- [ ] Testes automatizados (pytest, coverage >80%)
- [ ] Pipeline CI/CD (GitHub Actions)
- [ ] Rate limiting e autenticação JWT
- [ ] Persistência (PostgreSQL) para histórico e treinamento
- [ ] Processamento assíncrono para batches grandes (Celery + Redis)
- [ ] Suporte a mais idiomas (es, fr, de)
- [ ] Fine-tuning do modelo com feedback coletado

### **Operações e Deploy**
- [ ] Monitoramento com Prometheus + Grafana
- [ ] Alertas para rate limits da API Groq
- [ ] Health checks e métricas de uptime

**Referências de arquivos principais:**

**Backend:**
- [backend/app/main.py](backend/app/main.py) — ponto de entrada da API
- [backend/app/services.py](backend/app/services.py) — integração com LLM e orquestração
- [backend/app/utils.py](backend/app/utils.py) — pipeline de pré-processamento NLP
- [backend/app/schemas.py](backend/app/schemas.py) — modelos de request/response
- [backend/app/templates.py](backend/app/templates.py) — templates de respostas
- [backend/app/exceptions.py](backend/app/exceptions.py) — erros específicos do app

**Frontend:**
- [frontend/src/App.tsx](frontend/src/App.tsx) — componente principal
- [frontend/src/api.ts](frontend/src/api.ts) — cliente da API
- [frontend/src/types.ts](frontend/src/types.ts) — tipos TypeScript
- [frontend/src/components/](frontend/src/components/) — componentes React
- [frontend/src/utils/emailParser.ts](frontend/src/utils/emailParser.ts) — parser de arquivos

