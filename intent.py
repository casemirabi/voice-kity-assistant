import re
import unicodedata
from dataclasses import dataclass
from typing import Optional


@dataclass
class Query:
    intent: str
    keyword: Optional[str]
    max_price: Optional[float]


_money_re = re.compile(
    r"(até|ate|no máximo|no maximo|preço máximo|preco maximo|preço maximo|preco máximo|menos de|por até|por ate|preso máximo|preso maximo)\s*(r\$)?\s*([\d\.]+,\d{2}|[\d\.]+)",
    re.I
)


def _strip_accents(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def _normalize_speech(text: str) -> str:
    t = text.lower().strip()
    t = _strip_accents(t)

    replacements = {
        "floreta": "floratta",
        "florata": "floratta",
        "florattah": "floratta",
        "mal bake": "malbec",
        "malbek": "malbec",
        "mal beque": "malbec",
        "malbeck": "malbec",
        "preso maximo": "preco maximo",
        "preso maximo ": "preco maximo ",
        "preco maximo": "preco maximo",
    }

    for old, new in replacements.items():
        t = t.replace(old, new)

    t = re.sub(r"\s+", " ", t).strip()
    return t


def _clean_keyword(text: str) -> Optional[str]:
    text = _money_re.sub("", text)
    text = re.sub(
        r"\b(quero|procuro|tem|me mostra|recomenda|buscar|encontrar|pesquise|pesquisar|mostra|ache|achar)\b",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"\b(por nome|filtrar por nome|pesquisar por nome|preco maximo|preço maximo)\b",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(r"\s+", " ", text).strip(" .,-")
    return text if len(text) >= 2 else None


def parse_query(text: str) -> Query:
    t = _normalize_speech(text)

    if any(x in t for x in ["sair", "parar", "encerrar"]):
        return Query("sair", None, None)

    if any(x in t for x in ["atualizar catalogo", "atualizar produtos", "recarregar catalogo"]):
        return Query("atualizar", None, None)

    if any(x in t for x in ["por nome", "filtrar por nome", "pesquisar por nome"]):
        return Query("outro", None, None)

    max_price = None
    m = _money_re.search(t)
    if m:
        raw = m.group(3).replace(".", "").replace(",", ".")
        try:
            max_price = float(raw)
        except Exception:
            max_price = None

    keyword = _clean_keyword(t)

    if any(x in t for x in ["quero", "procuro", "tem", "me mostra", "recomenda", "buscar", "encontrar", "pesquise", "pesquisar", "mostra", "ache", "achar"]):
        return Query("buscar", keyword, max_price)

    # se falou algo útil sem verbo explícito, ainda tenta buscar
    if keyword:
        return Query("buscar", keyword, max_price)

    return Query("outro", keyword, max_price)