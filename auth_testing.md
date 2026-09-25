# Playbook de testes — Painel do clube (auth por senha única)

Implementação adotada (conforme playbook do integration_expert, versão mínima
para senha única de administração, sem contas de usuário):
- Senha única em `backend/.env` (`ADMIN_PASSWORD`), carregada com load_dotenv.
- Rotas do painel exigem header `x-admin-password`, comparado com
  `hmac.compare_digest` (evita timing attack). Sem cookie/JWT: o frontend
  guarda a senha em sessionStorage e envia no header.
- Sem dados de usuário no banco: nada de hash bcrypt necessário (não há
  senha de usuário armazenada; a senha vive só no .env).

## Testes (via URL externa do frontend)
```bash
API_URL=https://salto-snooker.preview.emergentagent.com

# 1. Login correto
curl -s -X POST "$API_URL/api/admin/login" -H "x-admin-password: FlavioSnoocker2026"
# esperado: {"ok":true}

# 2. Login errado (deve dar 401)
curl -s -o /dev/null -w "%{http_code}" -X POST "$API_URL/api/admin/login" -H "x-admin-password: errada"
# esperado: 401

# 3. Listar campeonatos (público)
curl -s "$API_URL/api/campeonatos"

# 4. Criar campeonato (admin)
curl -s -X POST "$API_URL/api/admin/campeonatos" -H "x-admin-password: FlavioSnoocker2026" \
  -H "Content-Type: application/json" -d '{"title":"Copa Teste"}'

# 5. Registrar inscrição (público) e ler no painel
curl -s -X POST "$API_URL/api/inscricoes" -H "Content-Type: application/json" \
  -d '{"modalidade":"Um time","nome":"Dupla Teste","idade":25,"sexo":"Masculino","campeonato":"Copa Teste","telefone":"11999999999","cidade":"Salto/SP"}'
curl -s "$API_URL/api/admin/inscricoes" -H "x-admin-password: FlavioSnoocker2026"
```

Credenciais em `/app/memory/test_credentials.md`.
