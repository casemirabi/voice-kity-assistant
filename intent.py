import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class Query:
    intent: str                 # "buscar" | "atualizar" | "sair" | "outro"
    keyword: Optional[str]
    max_price: Optional[float]

_money_re = re.compile(r"(até|ate|no máximo|no maximo|menos de)\s*(r\$)?\s*([\d\.]+,\d{2}|[\d\.]+)", re.I)

def parse_query(text: str) -> Query:
    t = text.strip().lower()

    if any(x in t for x in ["sair", "parar", "encerrar"]):
        return Query("sair", None, None)

    if any(x in t for x in ["atualizar catálogo", "atualizar catalogo", "atualizar produtos", "recarregar catálogo", "recarregar catalogo"]):
        return Query("atualizar", None, None)

    max_price = None
    m = _money_re.search(t)
    if m:
        raw = m.group(3).replace(".", "").replace(",", ".")
        try:
            max_price = float(raw)
        except:
            max_price = None

    # keyword: remove trecho de preço
    keyword = _money_re.sub("", t).strip()
    keyword = keyword if len(keyword) >= 3 else None

    if any(x in t for x in ["quero", "procuro", "tem", "me mostra", "recomenda", "buscar", "encontrar"]):
        return Query("buscar", keyword, max_price)

    return Query("outro", keyword, max_price)
