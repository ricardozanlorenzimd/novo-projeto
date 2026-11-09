# CLAUDE.md

Site pessoal do Ricardo Zanlorenzi, ainda em esqueleto: três páginas (`index.html`, `projects.html`, `contato.html`) em HTML + CSS puro, sem build e sem dependências. No ar em https://novo-projeto-ashen.vercel.app/ (repositório `novo-projeto` no GitHub; a Vercel publica a cada `git push` na `main`). O remote `antigo` é o site anterior (minha-primeira-pagina-wine.vercel.app) — nunca dê push nele sem o dono pedir. O dono é iniciante: explique em português simples.

## Comandos

- **Abrir:** `open index.html` (atualize o navegador depois de editar)
- **Testar:** `python3 -I .claude/scripts/check_site.py` — links quebrados (com maiúsculas exatas) e menu em todas as páginas. Rode antes de todo commit.
- **Publicar:** `/publicar [mensagem]` — testa, faz commit, `git push` e confere o site no ar com `curl`.

## Convenções

- Todo texto do site em **português do Brasil**, primeira pessoa.
- Toda página tem o mesmo `<nav class="menu">`, com `aria-current="page"` na página atual. Página nova → entra no menu de **todos** os `.html` e na lista `MENU` de `check_site.py`.
- Estilos comuns em `style.css`; estilo de uma página só fica no `<style>` dela.
- Se uma página ganhar JS: `var`, `textContent` (nunca `innerHTML` com dados), comentários em português.
- Um hook arruma os espaços de todo `.html` editado — não precisa formatar à mão.
- Planeje antes (arquivos + ordem) e trabalhe em blocos pequenos com pausa para revisão quando o dono pedir.
