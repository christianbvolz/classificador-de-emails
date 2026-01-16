# Classificador de Email

**Visão Geral:**
- **Contexto:** Este repositório contém uma solução para classificar emails em **Produtivo** ou **Improdutivo** e gerar respostas automáticas, conforme descrito em [contextoDesafio.md](contextoDesafio.md).

**O que foi implementado até agora:**
- **Backend API:** endpoint FastAPI em [app/main.py](app/main.py) expõe `POST /process-email` para receber texto de email e retornar a análise.
- **Pipeline de NLP:** pré-processamento em [app/utils.py](app/utils.py) (remoção de ruído, detecção de idioma com `langdetect`, lematização via spaCy quando o modelo está disponível).
- **Integração com LLM:** orquestração para classificação e geração de resposta em [app/services.py](app/services.py) usando o cliente Groq para chamar um modelo Llama-3.
- **Schemas:** modelos de requisição/resposta com `pydantic` em [app/schemas.py](app/schemas.py).
- **Tratamento de erros:** exceções customizadas em [app/exceptions.py](app/exceptions.py) para falhas de NLP e do provedor LLM.
- **Dependências:** arquivo [requirements.txt](requirements.txt) com bibliotecas principais (FastAPI, Groq, spaCy, langdetect, python-dotenv, uvicorn).

**O que NÃO foi implementado / pendente:**
- Interface web (HTML) para upload de arquivos ou input direto de texto;
- Parsing de arquivos `.pdf` e `.txt` no upload (atualmente a API recebe texto bruto);
- Testes automatizados e pipeline CI/CD;
- Deploy público (é possível rodar localmente ou em container conforme Dockerfile existente).

**Como rodar localmente (rápido):**
1. Copie o repositório e acesse a pasta:

   pip install -r requirements.txt

2. Crie um arquivo `.env` com sua chave Groq API:

   GROQ_API_KEY=seu_token_aqui

3. Instale os modelos spaCy necessários (se desejar lematização completa):

   python -m spacy download en_core_web_sm
   python -m spacy download pt_core_news_sm

4. Inicie a API:

   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

5. Exemplo de uso via `curl`:

   curl -X POST "http://localhost:8000/process-email" -H "Content-Type: application/json" -d '{"content": "Olá, preciso de ajuda com minha fatura."}'

**Observações técnicas importantes:**
- O código atualmente chama a API Groq (`groq` client). Garanta que `GROQ_API_KEY` esteja configurada.
- A pipeline de NLP tenta carregar modelos spaCy; se o modelo não existir, há um fallback simples de limpeza de texto.
- A resposta do LLM é esperada em JSON estrito contendo `is_productive`, `suggested_subject` e `suggested_body`.

---

## Técnicas de Prompt Engineering Aplicadas

Para maximizar a qualidade das respostas geradas pela IA, foram aplicadas as seguintes técnicas de engenharia de prompt:

### 1. **Few-Shot Learning com Templates Dinâmicos**
- Exemplos de classificação e resposta são gerados automaticamente a partir de `RESPONSE_TEMPLATES`
- Fornece à IA padrões concretos de respostas produtivas e improdutivas em português e inglês
- Mantém consistência: templates usados como exemplos são os mesmos usados como fallback

### 2. **Estrutura de Contexto Hierárquica**
O prompt segue um fluxo lógico de raciocínio:
1. **Category identification** — identifica primeiro a categoria do email (payment_issue, technical_support, etc.)
2. **Perspective** — define quem está respondendo (Support Team)
3. **Tone** — estabelece tom profissional e empático
4. **Personalization** — instrui a usar detalhes específicos do email
5. **Structure** — define organização (3 parágrafos: saudação, conteúdo, fechamento)
6. **Length** — limita tamanho (100-250 palavras)

### 3. **Instruções Claras de Output**
- Define exatamente o que cada campo deve conter (`is_productive`, `suggested_subject`, `suggested_body`)
- Especifica formato de retorno estrito (JSON com chaves específicas)
- Usa `response_format={"type": "json_object"}` para garantir parsing confiável

### 4. **Temperatura Otimizada**
- `temperature=0.3` — equilíbrio entre criatividade e consistência
- Baixa o suficiente para respostas previsíveis, alta o suficiente para personalização

### 5. **Validação e Fallback Robusto**
- Valida campos obrigatórios e tamanho mínimo de conteúdo
- Em caso de falha de validação ou erro de parsing, usa templates pré-definidos
- Garante que a API sempre retorna uma resposta válida

### 6. **Envio de Contexto Duplo**
- Envia tanto o email original quanto o texto limpo (lematizado)
- Permite que a IA use detalhes originais (nomes, números) para personalização
- Usa texto limpo para melhor compreensão semântica

### 7. **Limitação de Tokens**
- `max_tokens=800` — controla custo e previne respostas excessivamente longas
- Combinado com instrução de tamanho no prompt (100-250 palavras)

### 8. **Logging e Monitoramento**
- Registra tokens consumidos, idioma detectado e classificação
- Permite análise de custos, performance e padrões de uso
- Facilita debugging e otimizações futuras

---

**Próximos passos:**
- Implementar a interface web (upload `.pdf` / `.txt` e campo de texto) e integrá-la com a API;
- Adicionar parsing robusto de PDFs e attachments;
- Cobrir com testes unitários e de integração;
- Preparar Dockerfile/compose para deploy e publicar em um serviço (Render/Heroku/Spaces).

**Referências de arquivos principais:**
- [app/main.py](app/main.py) — ponto de entrada da API
- [app/services.py](app/services.py) — integração com LLM e orquestração
- [app/utils.py](app/utils.py) — pipeline de pré-processamento NLP
- [app/schemas.py](app/schemas.py) — modelos de request/response
- [app/exceptions.py](app/exceptions.py) — erros específicos do app

