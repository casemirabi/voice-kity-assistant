import re
from dataclasses import dataclass
from typing import List, Optional

import pdfplumber


@dataclass
class Product:
    name: str
    price: float
    url: str = ""


price_re = re.compile(r"R\$\s*([\d\.]+,\d{2})", re.I)


def parse_price(text: str) -> Optional[float]:
    m = price_re.search(text)
    if not m:
        return None
    return float(m.group(1).replace(".", "").replace(",", "."))


def normalize_name(name: str) -> str:
    name = re.sub(r"\s+", " ", name).strip(" -–•\t")
    return name


def is_valid_product_name(name: str) -> bool:
    name_l = name.lower().strip()

    invalid_terms = [
        " cm",
        "x ",
        " x ",
        "cada",
        "dimensões",
        "dimensao",
        "caixa",
        "sacola",
        "envelope",
        "r$",
        "página",
        "pagina",
        "leve",
        "por:",
        "economize",
        "lançamento",
        "lancamento",
        "edição limitada",
        "edicao limitada",
        "acompanha varetas",
        "escolha a sua",
        "opções de cores",
        "opcoes de cores",
    ]

    valid_keywords = [
        "kit",
        "presente",
        "perfume",
        "creme",
        "hidratante",
        "sabonete",
        "colônia",
        "colonia",
        "body splash",
        "body spray",
        "gel",
        "óleo",
        "oleo",
        "loção",
        "locao",
        "eau de parfum",
        "desodorante",
        "difusor",
        "aromatizador",
        "vela",
        "refil",
        "palette",
        "batom",
        "primer",
        "máscara",
        "mascara",
        "gloss",
        "shower gel",
    ]

    if len(name_l) < 5:
        return False

    if any(term in name_l for term in invalid_terms):
        return False

    if re.fullmatch(r"[\d\s,\.xX\-]+", name_l):
        return False

    return any(term in name_l for term in valid_keywords)


def dedupe_products(products: List[Product]) -> List[Product]:
    best_by_name = {}

    for p in products:
        key = p.name.lower().strip()
        if key not in best_by_name:
            best_by_name[key] = p
        else:
            # mantém o menor preço para o mesmo nome
            if p.price < best_by_name[key].price:
                best_by_name[key] = p

    return sorted(best_by_name.values(), key=lambda x: (x.name.lower(), x.price))


def load_catalog_from_pdf(path: str) -> List[Product]:
    products: List[Product] = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = [normalize_name(line) for line in text.split("\n") if line.strip()]

            for i, line in enumerate(lines):
                price = parse_price(line)
                if price is None:
                    continue

                # tenta encontrar um nome válido nas 3 linhas anteriores
                candidates = []
                for back in range(1, 4):
                    idx = i - back
                    if idx >= 0:
                        candidate = normalize_name(lines[idx])
                        if is_valid_product_name(candidate):
                            candidates.append(candidate)

                if not candidates:
                    continue

                # pega o candidato mais próximo do preço
                name = candidates[0]

                products.append(Product(
                    name=name,
                    price=price,
                    url=""
                ))

    return dedupe_products(products)