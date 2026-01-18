# 🔧 Atualizar Configuração no Render

## ⚠️ IMPORTANTE: Mudança de Estrutura

O projeto foi reorganizado em **monorepo**. O backend agora está na pasta `backend/`.

---

## 📋 Passos para Atualizar no Render

### **Opção 1: Atualizar Service Existente (Recomendado)**

1. **Acesse seu service no Render:**
   - https://dashboard.render.com
   - Clique no service: `email-classifier-api`

2. **Vá em "Settings"** (menu lateral esquerdo)

3. **Na seção "Build & Deploy":**
   - Encontre: **"Root Directory"**
   - Mude de: ` ` (vazio) ou `.`
   - Para: `backend` ⚠️ **OBRIGATÓRIO**

4. **Salve as mudanças:**
   - Role até o final da página
   - Clique em **"Save Changes"**

5. **Trigger Manual Deploy:**
   - Volte para aba "Deploys"
   - Clique em **"Manual Deploy"** → **"Deploy latest commit"**
   - Aguarde ~5-8 minutos

---

### **Opção 2: Criar Novo Service (Se Preferir)**

Se quiser começar do zero:

1. **Dashboard** → **"New +"** → **"Web Service"**
2. Conecte o repositório: `classificador-de-email`
3. **Configure:**
   ```
   Name: email-classifier-api
   Region: Oregon
   Branch: main
   Root Directory: backend          ← IMPORTANTE!
   Runtime: Docker
   Dockerfile Path: ./Dockerfile
   Docker Context: .
   Instance Type: Free
   ```
4. **Environment Variables:**
   ```
   GROQ_API_KEY = [sua_chave]
   ```
5. **Create Web Service**

---

## ✅ Verificar se Funcionou

Após deploy concluído, teste:

```bash
# Health check
curl https://classificador-de-emails-qts5.onrender.com/health

# Deve retornar:
{"status":"healthy","service":"email-classifier"}
```

---

## 🐛 Se Der Erro

### **Erro: "No such file or directory: Dockerfile"**

**Causa:** Root Directory não configurado como `backend`

**Solução:**
1. Settings → Build & Deploy
2. Root Directory = `backend`
3. Save Changes → Manual Deploy

### **Erro: "Build failed"**

**Causa:** Paths incorretos

**Verificar:**
- Root Directory = `backend` ✓
- Dockerfile Path = `./Dockerfile` ✓
- Docker Context = `.` ✓

---

## 📊 Configuração Final Correta

| Campo | Valor |
|-------|-------|
| Root Directory | `backend` |
| Runtime | Docker |
| Dockerfile Path | `./Dockerfile` |
| Docker Context | `.` |
| Environment | `GROQ_API_KEY` |

---

## 🎉 Pronto!

Após atualizar, o Render vai:
1. Ler arquivos de `backend/` ao invés da raiz
2. Fazer build do Docker normalmente
3. Deploy funciona exatamente como antes
4. URL permanece a mesma

**Nada muda para o usuário final!** Apenas a organização interna do repositório.
