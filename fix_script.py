"""Corrige o bloco problemático do organizar.py usando números de linha."""

with open("organizar.py", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

# Encontra o início e fim do bloco fixes
start = None
end = None
for i, line in enumerate(lines):
    if "# Corrige encoding quebrado" in line:
        start = i
    if start is not None and i > start and line.strip() == "}":
        end = i
        break

if start is None or end is None:
    print(f"Bloco nao encontrado: start={start}, end={end}")
    exit(1)

print(f"Substituindo linhas {start+1} a {end+1}")

# Novo bloco usando chr() para evitar qualquer char especial no source
novo_bloco = [
    "    # Corrige encoding quebrado comum (latin-1 lido como UTF-8)\n",
    "    fixes = {\n",
    "        b'\\xc3\\xa9'.decode(): chr(233),  # e com acento agudo\n",
    "        b'\\xc3\\xa3'.decode(): chr(227),  # a com til\n",
    "        b'\\xc3\\xa7'.decode(): chr(231),  # c cedilha\n",
    "        b'\\xc3\\xa1'.decode(): chr(225),  # a com acento agudo\n",
    "        b'\\xc3\\xa0'.decode(): chr(224),  # a com acento grave\n",
    "        b'\\xc3\\xad'.decode(): chr(237),  # i com acento agudo\n",
    "        b'\\xc3\\xb3'.decode(): chr(243),  # o com acento agudo\n",
    "        b'\\xc3\\xba'.decode(): chr(250),  # u com acento agudo\n",
    "        b'\\xc3\\x89'.decode(): chr(201),  # E maiusculo acento agudo\n",
    "        b'\\xc3\\x93'.decode(): chr(211),  # O maiusculo acento agudo\n",
    "        b'\\xc3\\x87'.decode(): chr(199),  # C maiusculo cedilha\n",
    "        b'\\xc3\\x95'.decode(): chr(213),  # O maiusculo til\n",
    "        b'\\xc3\\xb5'.decode(): chr(245),  # o com til\n",
    "        b'\\xc3\\x9c'.decode(): chr(220),  # U maiusculo dierese\n",
    "        b'\\xc3\\x9a'.decode(): chr(218),  # U maiusculo acento agudo\n",
    "        b'\\xe2\\x80\\x9c'.decode(): chr(34),   # aspas esquerda\n",
    "        b'\\xe2\\x80\\x9d'.decode(): chr(34),   # aspas direita\n",
    "        b'\\xe2\\x80\\x99'.decode(): chr(39),   # apostrofe\n",
    "        b'\\xe2\\x80\\x94'.decode(): chr(8212), # traco longo\n",
    "        b'\\xe2\\x80\\x93'.decode(): chr(8211), # traco medio\n",
    "        b'\\xc2\\xb0'.decode(): chr(176),  # grau\n",
    "        b'\\xc2\\xb2'.decode(): chr(178),  # quadrado\n",
    "        b'\\xc2\\xb3'.decode(): chr(179),  # cubico\n",
    "        b'\\xc2\\xb7'.decode(): chr(183),  # ponto medio\n",
    "    }\n",
]

new_lines = lines[:start] + novo_bloco + lines[end+1:]

with open("organizar.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Corrigido com sucesso.")
