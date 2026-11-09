---
description: Verifica o site, faz commit, envia ao GitHub e confere o site no ar
argument-hint: [mensagem do commit, opcional]
---

Publique as mudanças atuais do site. Responda em português, em linguagem simples. Pare e explique se qualquer passo falhar — não tente contornar.

1. **Verificar antes.** Rode `python3 -I .claude/scripts/check_site.py`. Se ele encontrar problemas, liste-os e **pare** sem fazer commit.
2. **Mostrar o que vai subir.** Rode `git status --short` e resuma em uma lista o que mudou em cada arquivo. Se não houver mudanças, diga isso e pare.
3. **Procurar senhas.** Rode `git diff` e `git diff --cached` e confirme que não aparece nenhum token (`ghp_`, `github_pat_`, `sk-`) nem arquivo `.env`. Se aparecer, pare e avise.
4. **Commit.** `git add -A` e commit com a mensagem "$ARGUMENTS". Se ela estiver vazia, escreva uma mensagem curta em português dizendo o que mudou. Termine a mensagem com a linha de coautoria do Claude.
5. **Enviar.** `git push origin main` (nunca no remote `antigo`). Se pedir senha ou falhar, mostre o erro e pare.
6. **Conferir no ar.** Espere a Vercel publicar (cerca de 1 minuto) e confira com `curl` que https://novo-projeto-ashen.vercel.app/ e cada página do menu respondem 200 em HTTPS.
7. **Relatar** em poucas linhas: o commit (hash e mensagem), o resultado da verificação e o link do site.
