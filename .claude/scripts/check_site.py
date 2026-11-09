"""Verifica todas as páginas do site: links quebrados e menus faltando.

Uso (na pasta do site):  python3 -I .claude/scripts/check_site.py
Sai com código 0 se estiver tudo certo, 1 se encontrar problemas.
"""

import os
import re
import sys
from html.parser import HTMLParser

PASTA = os.getcwd()

# O menu esperado, na ordem em que deve aparecer em todas as páginas
MENU = [
    ("index.html", "Início"),
    ("projects.html", "Projetos"),
    ("contato.html", "Contato"),
]


class LeitorDePagina(HTMLParser):
    """Coleta links, ids e o conteúdo de cada <nav class="menu">."""

    def __init__(self):
        super().__init__()
        self.links = []          # (atributo, valor, linha)
        self.ids = set()
        self.menus = []          # cada menu: lista de (href, texto, atual)
        self._no_menu = False
        self._link_atual = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        linha = self.getpos()[0]
        if "id" in a:
            self.ids.add(a["id"])
        for nome in ("href", "src"):
            if a.get(nome):
                self.links.append((nome, a[nome], linha))
        if tag == "nav" and "menu" in (a.get("class") or "").split():
            self._no_menu = True
            self.menus.append([])
        elif tag == "a" and self._no_menu:
            self._link_atual = [a.get("href", ""), "", a.get("aria-current") == "page"]

    def handle_data(self, data):
        if self._link_atual is not None:
            self._link_atual[1] += data

    def handle_endtag(self, tag):
        if tag == "a" and self._link_atual is not None:
            href, texto, atual = self._link_atual
            self.menus[-1].append((href, texto.strip(), atual))
            self._link_atual = None
        elif tag == "nav" and self._no_menu:
            self._no_menu = False


def existe_exatamente(caminho):
    """Como os servidores: diferencia maiúsculas de minúsculas (o Mac não)."""
    partes = os.path.normpath(caminho).split(os.sep)
    atual = PASTA
    for parte in partes:
        if parte in ("", "."):
            continue
        if not os.path.isdir(atual) or parte not in os.listdir(atual):
            return False
        atual = os.path.join(atual, parte)
    return True


def main():
    paginas = sorted(f for f in os.listdir(PASTA) if f.endswith(".html"))
    leitores = {}
    for pagina in paginas:
        leitor = LeitorDePagina()
        with open(os.path.join(PASTA, pagina), encoding="utf-8") as arquivo:
            leitor.feed(arquivo.read())
        leitores[pagina] = leitor

    problemas = []
    externos = set()

    for pagina, leitor in leitores.items():
        # ---- 1. Links quebrados ----
        for atributo, valor, linha in leitor.links:
            if re.match(r"^(mailto|tel|javascript|data):", valor):
                continue
            if re.match(r"^https?://", valor):
                externos.add(valor)
                continue
            if valor.startswith("/api/"):
                # Função do servidor: só existe no site publicado
                arquivo_api = valor[1:].split("?")[0] + ".js"
                if not existe_exatamente(arquivo_api):
                    problemas.append(f"{pagina}:{linha} — {atributo}=\"{valor}\": não existe {arquivo_api}")
                continue
            alvo, _, ancora = valor.partition("#")
            alvo = alvo.split("?")[0].lstrip("/")
            if alvo and not existe_exatamente(alvo):
                problemas.append(f"{pagina}:{linha} — {atributo}=\"{valor}\": arquivo não existe (ou maiúsculas/minúsculas diferentes)")
                continue
            if ancora:
                destino = leitores.get(alvo or pagina)
                if destino is not None and ancora not in destino.ids:
                    problemas.append(f"{pagina}:{linha} — {atributo}=\"{valor}\": não há id=\"{ancora}\" na página")

        # ---- 2. Menu ----
        if len(leitor.menus) == 0:
            problemas.append(f"{pagina} — sem <nav class=\"menu\">")
            continue
        if len(leitor.menus) > 1:
            problemas.append(f"{pagina} — tem {len(leitor.menus)} menus (deveria ter 1)")
        menu = leitor.menus[0]
        encontrado = [(href, texto) for href, texto, _ in menu]
        if encontrado != MENU:
            esperado = " · ".join(f"{t} ({h})" for h, t in MENU)
            atual = " · ".join(f"{t} ({h})" for h, t in encontrado) or "(vazio)"
            problemas.append(f"{pagina} — menu diferente do padrão\n      esperado: {esperado}\n      encontrado: {atual}")
        marcados = [href for href, _, atual in menu if atual]
        if marcados != [pagina] and pagina in dict(MENU):
            problemas.append(f"{pagina} — aria-current=\"page\" deveria estar só em {pagina}; está em: {', '.join(marcados) or 'nenhum'}")

    # ---- 3. Páginas fora do menu ----
    no_menu = {href for href, _ in MENU}
    for pagina in paginas:
        if pagina not in no_menu:
            problemas.append(f"{pagina} — página existe, mas não está no menu")
    for href, _ in MENU:
        if href not in leitores:
            problemas.append(f"menu aponta para {href}, mas o arquivo não existe")

    # ---- Relatório ----
    total_links = sum(len(l.links) for l in leitores.values())
    print(f"Páginas verificadas: {len(paginas)} ({', '.join(paginas)})")
    print(f"Links e scripts verificados: {total_links}")
    if externos:
        print(f"Links externos (não testados): {len(externos)}")
        for url in sorted(externos):
            print(f"  - {url}")
    if problemas:
        print(f"\nPROBLEMAS ENCONTRADOS: {len(problemas)}")
        for p in problemas:
            print(f"  ✗ {p}")
        return 1
    print("\nTudo certo: nenhum link quebrado e todos os menus completos. ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
