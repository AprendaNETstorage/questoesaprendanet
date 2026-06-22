"""
Organiza, classifica e padroniza questões HTML de física ENEM.
Uso: python organizar.py
"""

import os
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from collections import defaultdict

# ─── Configuração ────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
DEST = BASE_DIR

FONTES = [
    Path(r"C:\Users\SAMUEL\Documents\GitHub\Questoes_AprendaNET"),
    Path(r"C:\Users\SAMUEL\Documents\GitHub\Questoesfisica"),
    Path(r"C:\Users\SAMUEL\Documents\GitHub\Lista03enem"),
    Path(r"C:\Users\SAMUEL\Documents\GitHub\Quest-es-Celso"),
]

# Matérias e palavras-chave (ordem importa: mais específico primeiro)
MATERIAS = {
    "optica": [
        "óptica", "optica", "lente", "espelho", "refração", "refraçao", "reflexão",
        "reflexao", "difração", "difraçao", "prisma", "índice de refração",
        "convergente", "divergente", "foco", "imagem real", "imagem virtual",
        "câmara escura", "olho", "miopia", "hipermetropia",
    ],
    "ondulatoria": [
        "ondulatória", "ondulat", "onda", "frequência", "comprimento de onda",
        "amplitude", "período", "som", "acústica", "doppler", "infrassom",
        "ultrassom", "ressonância", "nó", "ventre", "estacionária",
    ],
    "eletricidade": [
        "corrente elétrica", "tensão elétrica", "resistência elétrica", "circuito",
        "ohm", "potência elétrica", "capacitor", "campo elétrico", "eletrostática",
        "carga elétrica", "coulomb", "elétron", "condutor", "isolante", "resistor",
        "voltagem", "amperímetro", "voltímetro", "transformador", "gerador",
        "eletromagnetismo", "indução", "campo magnético", "força magnética",
    ],
    "termologia": [
        "temperatura", "calor", "termologia", "termodinâmica", "termodinamica",
        "dilatação", "dilataçao", "gás", "gas", "pressão", "volume",
        "lei dos gases", "lei de boyle", "lei de charles", "ciclo de carnot",
        "entropia", "isotérmica", "adiabática", "capacidade calorífica",
        "calor específico", "fusão", "vaporização", "ebulição", "sublimação",
    ],
    "quantidade_movimento": [
        "quantidade de movimento", "impulso", "colisão", "coliçao", "conservação do momento",
        "momento linear", "choque", "elástico", "inelástico", "explosão",
    ],
    "torque": [
        "torque", "momento de força", "equilíbrio", "alavanca", "centro de massa",
        "centro de gravidade", "estática", "braço da força", "rolamento",
    ],
    "energia": [
        "energia cinética", "energia potencial", "trabalho", "potência",
        "conservação de energia", "energia mecânica", "energia total",
        "joule", "watt", "rendimento", "eficiência energética", "energia elétrica",
        "energia térmica",
    ],
    "leis_newton": [
        "força", "newton", "atrito", "força normal", "peso", "inércia",
        "2ª lei", "3ª lei", "ação e reação", "força resultante", "aceleração",
        "massa", "dinâmica", "plano inclinado",
    ],
    "cinematica": [
        "velocidade", "deslocamento", "trajetória", "mru", "mruv",
        "queda livre", "lançamento", "posição", "espaço", "tempo",
        "aceleração da gravidade", "movimento uniforme", "movimento retilíneo",
        "gráfico espaço", "gráfico velocidade",
    ],
}

NOME_BONITO = {
    "cinematica": "Cinemática",
    "leis_newton": "Leis de Newton",
    "energia": "Energia",
    "quantidade_movimento": "Quantidade de Movimento",
    "torque": "Torque e Equilíbrio",
    "termologia": "Termologia",
    "ondulatoria": "Ondulatória",
    "optica": "Óptica",
    "eletricidade": "Eletricidade",
    "fisica": "Física (Geral)",
}

# ─── Parser HTML simples ──────────────────────────────────────────────────────

class LeitorHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.titulo = ""
        self.texto = []
        self.imagens = []
        self.em_title = False
        self.em_style = False
        self.em_script = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.em_title = True
        elif tag == "style":
            self.em_style = True
        elif tag == "script":
            self.em_script = True
        elif tag == "img" and "src" in attrs:
            src = attrs["src"]
            if not src.startswith("http"):
                self.imagens.append(src)

    def handle_endtag(self, tag):
        if tag == "title":
            self.em_title = False
        elif tag == "style":
            self.em_style = False
        elif tag == "script":
            self.em_script = False

    def handle_data(self, data):
        if self.em_title:
            self.titulo += data
        elif not self.em_style and not self.em_script:
            self.texto.append(data)

    def texto_completo(self):
        return " ".join(self.texto).lower()


def ler_html(caminho: Path):
    try:
        conteudo = caminho.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None, "", []
    p = LeitorHTML()
    p.feed(conteudo)
    return conteudo, p.titulo.strip(), p.imagens


# ─── Classificação ───────────────────────────────────────────────────────────

def classificar(titulo: str, texto: str, pasta_origem: str) -> str:
    # Tenta pela pasta de origem primeiro (Questoes_AprendaNET já tem estrutura)
    pasta_map = {
        "cinematica": "cinematica",
        "eletricidade": "eletricidade",
        "energia": "energia",
        "leis_newton": "leis_newton",
        "ondulatoria": "ondulatoria",
        "optica": "optica",
        "quantidade_movimento": "quantidade_movimento",
        "termologia": "termologia",
        "torque": "torque",
    }
    for parte in pasta_origem.lower().replace("\\", "/").split("/"):
        if parte in pasta_map:
            return pasta_map[parte]

    combinado = (titulo + " " + texto).lower()

    pontos = defaultdict(int)
    for materia, palavras in MATERIAS.items():
        for palavra in palavras:
            if palavra in combinado:
                pontos[materia] += 1

    if pontos:
        return max(pontos, key=pontos.get)

    return "fisica"


# ─── CSS padrão ──────────────────────────────────────────────────────────────

CSS = """:root {
  --primary: #2c5f8a;
  --primary-hover: #1e4266;
  --bg: #f8f9fa;
  --card: #ffffff;
  --text: #1a1a1a;
  --border: #dee2e6;
  --correct: #d4edda;
  --wrong: #f8d7da;
  --radius: 8px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Segoe UI', Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  padding: 20px;
}

.container {
  max-width: 860px;
  margin: 0 auto;
  background: var(--card);
  border-radius: var(--radius);
  padding: 32px;
  border: 1px solid var(--border);
}

/* Navegação */
.nav {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.nav a, .btn {
  text-decoration: none;
  background: var(--primary);
  color: #fff;
  padding: 6px 14px;
  border-radius: var(--radius);
  font-size: 14px;
  border: none;
  cursor: pointer;
  transition: background 0.2s;
}

.nav a:hover, .btn:hover { background: var(--primary-hover); }

.nav .home {
  background: transparent;
  color: var(--primary);
  border: 1px solid var(--primary);
}
.nav .home:hover { background: var(--primary); color: #fff; }

.nav .spacer { flex: 1; }

/* Enunciado */
h2 { font-size: 1.1rem; color: var(--primary); margin-bottom: 16px; }
h3 { font-size: 1rem; margin: 16px 0 8px; }

p { margin: 10px 0; }

img { max-width: 100%; border-radius: 4px; margin: 8px 0; }

table {
  border-collapse: collapse;
  margin: 12px 0;
  width: 100%;
}
th, td {
  border: 1px solid var(--border);
  padding: 8px 12px;
  text-align: center;
}
th { background: var(--bg); }

/* Alternativas */
.opcoes { margin: 20px 0; }

.opcao {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 14px;
  border-radius: var(--radius);
  margin: 6px 0;
  cursor: pointer;
  border: 1px solid var(--border);
  transition: background 0.15s;
}
.opcao:hover { background: #e8f0f8; }

.circulo {
  width: 30px;
  height: 30px;
  min-width: 30px;
  background: var(--primary);
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 15px;
}

.feedback { font-weight: bold; margin-left: 6px; }

/* Inputs de resposta */
input[type=text] {
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 1rem;
  width: 120px;
  text-align: center;
}

.correto { background: var(--correct) !important; }
.errado  { background: var(--wrong)   !important; }

#mensagem { font-weight: bold; margin-top: 16px; font-size: 1.05rem; }

/* Index raiz */
.grade-materias {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
  margin-top: 24px;
}

.card-materia {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  text-decoration: none;
  color: var(--text);
  transition: box-shadow 0.2s, transform 0.2s;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.card-materia:hover {
  box-shadow: 0 4px 16px rgba(44,95,138,.15);
  transform: translateY(-2px);
}
.card-materia .icone { font-size: 2rem; }
.card-materia .nome { font-weight: 600; font-size: 1rem; }
.card-materia .qtd  { font-size: 0.85rem; color: #666; }

/* Index de matéria */
.lista-questoes { margin-top: 20px; }
.item-questao {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  margin: 6px 0;
  text-decoration: none;
  color: var(--text);
  transition: background 0.15s;
}
.item-questao:hover { background: #e8f0f8; }
.item-questao .num {
  width: 36px;
  height: 36px;
  min-width: 36px;
  background: var(--primary);
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 13px;
}
"""

ICONES = {
    "cinematica": "",
    "leis_newton": "",
    "energia": "",
    "quantidade_movimento": "",
    "torque": "",
    "termologia": "",
    "ondulatoria": "",
    "optica": "",
    "eletricidade": "",
    "fisica": "",
}


# ─── Geração de HTML ─────────────────────────────────────────────────────────

def profundidade_para_raiz(materia: str) -> str:
    return "../"  # questoesaprendanet/<materia>/questao_XX.html → ../style.css


def reescrever_html(conteudo: str, titulo_questao: str, materia: str,
                    anterior: str, proximo: str, num: int, total: int) -> str:
    """Remove estilos inline e scripts antigos, padroniza estrutura."""

    # Extrai body
    body_match = re.search(r"<body[^>]*>(.*?)</body>", conteudo, re.DOTALL | re.IGNORECASE)
    body = body_match.group(1) if body_match else conteudo

    # Remove tags <style> e <link rel=stylesheet> do body
    body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.DOTALL | re.IGNORECASE)

    # Remove âncoras de navegação antigas (linhas com href questaoXX.html)
    body = re.sub(
        r'<p>\s*<a\s+href="questao\d+\.html"[^>]*>.*?</a>.*?</p>',
        "", body, flags=re.DOTALL | re.IGNORECASE
    )
    # Remove links soltos de navegação
    body = re.sub(
        r'<a\s+href="questao\d+\.html"[^>]*>.*?</a>',
        "", body, flags=re.DOTALL | re.IGNORECASE
    )

    # Substitui classes antigas por novas
    body = body.replace('class="option"', 'class="opcao"')
    body = body.replace('class="circle"', 'class="circulo"')

    # Corrige caminhos de imagem (remove prefixos de pasta de origem)
    body = re.sub(r'src="(?:imagem|img)/([^"]+)"', r'src="imagens/\1"', body)

    # Corrige encoding quebrado comum (latin-1 lido como UTF-8)
    fixes = {
        b'\xc3\xa9'.decode(): chr(233),  # e com acento agudo
        b'\xc3\xa3'.decode(): chr(227),  # a com til
        b'\xc3\xa7'.decode(): chr(231),  # c cedilha
        b'\xc3\xa1'.decode(): chr(225),  # a com acento agudo
        b'\xc3\xa0'.decode(): chr(224),  # a com acento grave
        b'\xc3\xad'.decode(): chr(237),  # i com acento agudo
        b'\xc3\xb3'.decode(): chr(243),  # o com acento agudo
        b'\xc3\xba'.decode(): chr(250),  # u com acento agudo
        b'\xc3\x89'.decode(): chr(201),  # E maiusculo acento agudo
        b'\xc3\x93'.decode(): chr(211),  # O maiusculo acento agudo
        b'\xc3\x87'.decode(): chr(199),  # C maiusculo cedilha
        b'\xc3\x95'.decode(): chr(213),  # O maiusculo til
        b'\xc3\xb5'.decode(): chr(245),  # o com til
        b'\xc3\x9c'.decode(): chr(220),  # U maiusculo dierese
        b'\xc3\x9a'.decode(): chr(218),  # U maiusculo acento agudo
        b'\xe2\x80\x9c'.decode(): chr(34),   # aspas esquerda
        b'\xe2\x80\x9d'.decode(): chr(34),   # aspas direita
        b'\xe2\x80\x99'.decode(): chr(39),   # apostrofe
        b'\xe2\x80\x94'.decode(): chr(8212), # traco longo
        b'\xe2\x80\x93'.decode(): chr(8211), # traco medio
        b'\xc2\xb0'.decode(): chr(176),  # grau
        b'\xc2\xb2'.decode(): chr(178),  # quadrado
        b'\xc2\xb3'.decode(): chr(179),  # cubico
        b'\xc2\xb7'.decode(): chr(183),  # ponto medio
    }
    for errado, certo in fixes.items():
        body = body.replace(errado, certo)

    raiz = profundidade_para_raiz(materia)
    nav_ant = f'<a href="{anterior}">&laquo; Anterior</a>' if anterior else '<span style="opacity:.4">&laquo; Anterior</span>'
    nav_prox = f'<a href="{proximo}">Próxima &raquo;</a>' if proximo else '<span style="opacity:.4">Próxima &raquo;</span>'

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titulo_questao} — {NOME_BONITO.get(materia, materia)}</title>
  <link rel="stylesheet" href="{raiz}style.css">
</head>
<body>
<div class="container">
  <nav class="nav">
    <a class="home" href="{raiz}index.html">Início</a>
    <a class="home" href="index.html">{NOME_BONITO.get(materia, materia)}</a>
    <span class="spacer"></span>
    {nav_ant}
    <span style="font-size:13px;color:#666">{num}/{total}</span>
    {nav_prox}
  </nav>
  <h2>{titulo_questao}</h2>
  {body.strip()}
</div>
</body>
</html>"""


def gerar_index_materia(materia: str, questoes: list[dict]) -> str:
    nome = NOME_BONITO.get(materia, materia)
    itens = ""
    for q in questoes:
        itens += f"""
    <a class="item-questao" href="{q['arquivo']}">
      <span class="num">{q['num']}</span>
      <span>{q['titulo']}</span>
    </a>"""

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{nome} — Questões ENEM</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body>
<div class="container">
  <nav class="nav">
    <a class="home" href="../index.html">Início</a>
    <span class="spacer"></span>
    <span style="font-size:13px;color:#666">{len(questoes)} questões</span>
  </nav>
  <h2>{nome}</h2>
  <div class="lista-questoes">{itens}
  </div>
</div>
</body>
</html>"""


def gerar_index_raiz(resumo: dict) -> str:
    cards = ""
    for materia, info in sorted(resumo.items(), key=lambda x: x[0]):
        nome = NOME_BONITO.get(materia, materia)
        qtd = info["qtd"]
        cards += f"""
    <a class="card-materia" href="{materia}/index.html">
      <span class="nome">{nome}</span>
      <span class="qtd">{qtd} questoes</span>
    </a>"""

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Questões ENEM — Física</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container">
  <h2 style="font-size:1.5rem;margin-bottom:8px;">Questões ENEM — Física</h2>
  <p style="color:#666">Selecione uma matéria para começar.</p>
  <div class="grade-materias">{cards}
  </div>
</div>
</body>
</html>"""


# ─── Principal ────────────────────────────────────────────────────────────────

def main():
    print("=== Organizador de Questões ENEM ===\n")

    # Coletar todos os HTMLs das fontes
    candidatos = []
    for fonte in FONTES:
        if not fonte.exists():
            print(f"[AVISO] Pasta não encontrada: {fonte}")
            continue
        for html in sorted(fonte.rglob("*.html")):
            # Ignora node_modules e .github
            if any(p in html.parts for p in ["node_modules", ".github"]):
                continue
            # Ignora index.html (serão regenerados)
            if html.name.lower() == "index.html":
                continue
            candidatos.append(html)

    print(f"Encontrados {len(candidatos)} HTMLs para processar.\n")

    # Classificar
    por_materia = defaultdict(list)
    for html in candidatos:
        conteudo, titulo, imagens = ler_html(html)
        if conteudo is None:
            continue
        p = LeitorHTML()
        p.feed(conteudo)
        texto = p.texto_completo()
        pasta_rel = str(html.parent).lower()
        materia = classificar(titulo, texto, pasta_rel)
        por_materia[materia].append({
            "origem": html,
            "conteudo": conteudo,
            "titulo": titulo or html.stem,
            "imagens": imagens,
        })

    # Processar por matéria
    resumo = {}
    for materia, questoes in por_materia.items():
        pasta_dest = DEST / materia
        pasta_dest.mkdir(exist_ok=True)
        (pasta_dest / "imagens").mkdir(exist_ok=True)

        # Ordenar por título numérico se possível
        def chave(q):
            m = re.search(r"(\d+)", q["titulo"])
            return int(m.group(1)) if m else 9999

        questoes.sort(key=chave)

        total = len(questoes)
        meta_questoes = []

        for i, q in enumerate(questoes):
            num = i + 1
            arquivo = f"questao_{num:03d}.html"
            ant = f"questao_{(num-1):03d}.html" if num > 1 else ""
            prox = f"questao_{(num+1):03d}.html" if num < total else ""

            # Copiar imagens
            for img_src in q["imagens"]:
                img_origem = q["origem"].parent / img_src
                if img_origem.exists():
                    shutil.copy2(img_origem, pasta_dest / "imagens" / img_origem.name)
                else:
                    # tenta sem subpasta
                    img_origem2 = q["origem"].parent.parent / img_src.split("/")[-1]
                    if img_origem2.exists():
                        shutil.copy2(img_origem2, pasta_dest / "imagens" / img_origem2.name)

            # Reescrever HTML
            html_final = reescrever_html(
                q["conteudo"], q["titulo"], materia, ant, prox, num, total
            )
            (pasta_dest / arquivo).write_text(html_final, encoding="utf-8")

            meta_questoes.append({"num": num, "arquivo": arquivo, "titulo": q["titulo"]})

        # Gerar index da matéria
        (pasta_dest / "index.html").write_text(
            gerar_index_materia(materia, meta_questoes), encoding="utf-8"
        )

        resumo[materia] = {"qtd": total}
        print(f"  [ok] {NOME_BONITO.get(materia, materia)}: {total} questoes")

    # Gerar index raiz
    (DEST / "index.html").write_text(gerar_index_raiz(resumo), encoding="utf-8")

    # Salvar CSS
    (DEST / "style.css").write_text(CSS, encoding="utf-8")

    total_geral = sum(v["qtd"] for v in resumo.values())
    print(f"\n[CONCLUIDO] {total_geral} questoes organizadas em {len(resumo)} materias.")
    print(f"Destino: {DEST}")
    print(f"Abra: {DEST / 'index.html'}")


if __name__ == "__main__":
    main()
