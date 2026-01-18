# Backend - Email Classifier API

API FastAPI para classificação de emails e geração de respostas automáticas usando IA (Llama 3.3 via Groq).

## 🚀 Deploy no Render

**URL Atual:** https://classificador-de-emails-qts5.onrender.com

### Configuração no Render:

1. **Root Directory:** `backend` ⚠️ **IMPORTANTE**
2. **Runtime:** Docker
3. **Dockerfile Path:** `./Dockerfile`
4. **Docker Context:** `.`
5. **Environment Variable:** `GROQ_API_KEY`

## 🏃 Rodar Localmente

### Com Docker:
```bash
cd backend
docker build -t email-classifier .
docker run -p 8000:8000 --env-file ../.env email-classifier
```

### Sem Docker:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload
```

## 📚 Documentação

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 🔑 Variáveis de Ambiente

Crie arquivo `.env` na raiz do projeto:
```env
GROQ_API_KEY=sua_chave_aqui
```

Obtenha sua chave em: https://console.groq.com/keys
