# Auditoria de seguranca preliminar

Data: 2026-07-30

| Item | Severidade | Acao nesta branch |
|---|---:|---|
| `backend/backups/*.json` com hashes e dados | Alta | Removido do conteudo atual |
| `backend/uploads/` com fotos/evidencias | Alta | Removido do conteudo atual |
| `SECRET_KEY` com fallback hardcoded | Alta | Removido |
| Senhas padrao em seed/testes | Alta | Substituidas por variaveis de ambiente |

## Pendencias

- Decidir se o repositorio deve permanecer publico.
- Aprovar limpeza de historico Git.
- Rotacionar qualquer credencial que possa ter sido usada fora de ambiente demo.
