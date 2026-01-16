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

