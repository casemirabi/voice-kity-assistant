import json
import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import List, Optional


@dataclass
class Product:
    name: str
    price: float
    url: str


def load_catalog(path: str = "catalog_cache.json") -> List[Product]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = []
    for it in data:
        name = it.get("name")
        price = it.get("price")
        url = it.get("url", "")
        if name and (price is not None):
            items.append(Product(name=name, price=float(price), url=url))
    return items


def _normalize(text: str) -> str:
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def _is_noise_name(name: str) -> bool:
    n = _normalize(name)

    noise_terms = [
        "dimensoes", "cm", "cada", "caixa", "sacola", "envelope",
        "pagina", "leve presente", "economize", "opcoes de cores",
        "escolha a sua", "acompanha varetas"
    ]
    if any(term in n for term in noise_terms):
        return True

    if len(n) < 4:
        return True

    return False


def _is_tiny_or_sample(name: str) -> bool:
    n = _normalize(name)
    bad_patterns = [
        r"\b4\s*ml\b",
        r"\b5\s*ml\b",
        r"\b10\s*ml\b",
        r"\bamostra\b",
        r"\bmini\b",
        r"\brefil\b",
        r"\btester\b",
        r"\bprova\b",
    ]
    return any(re.search(p, n) for p in bad_patterns)


def _score_product(product_name: str, query: str) -> float:
    pn = _normalize(product_name)
    qn = _normalize(query)

    if not pn or not qn:
        return 0.0

    p_words = pn.split()
    q_words = [w for w in qn.split() if len(w) >= 2]

    if not q_words:
        return 0.0

    score = 0.0

    if pn == qn:
        score += 120

    if pn.startswith(qn):
        score += 90

    if qn in pn:
        score += 70

    exact_hits = 0
    prefix_hits = 0
    fuzzy_hits = 0

    for qw in q_words:
        best_sim = 0.0
        matched_prefix = False
        matched_exact = False

        for pw in p_words:
            sim = _similar(qw, pw)
            best_sim = max(best_sim, sim)

            if qw == pw:
                matched_exact = True
            if pw.startswith(qw) or qw.startswith(pw):
                matched_prefix = True

        if matched_exact:
            exact_hits += 1
            score += 25
        elif matched_prefix:
            prefix_hits += 1
            score += 18
        elif best_sim >= 0.80:
            fuzzy_hits += 1
            score += 14
        elif best_sim >= 0.68:
            score += 8

    score += exact_hits * 5
    score += prefix_hits * 3
    score += fuzzy_hits * 2

    full_sim = _similar(qn, pn)
    score += full_sim * 25

    # bônus para itens mais “vendáveis”
    if "kit" in p_words:
        score += 8
    if "presente" in p_words:
        score += 8
    if "malbec" in p_words and "malbec" in qn:
        score += 20
    if "floratta" in p_words and "floratta" in qn:
        score += 20
    if "lily" in p_words and "lily" in qn:
        score += 20

    # penaliza nome quebrado ou miniatura
    if _is_tiny_or_sample(product_name):
        score -= 25

    if len(p_words) <= 2:
        score -= 2

    return score


def search_catalog(
    items: List[Product],
    keyword: Optional[str],
    max_price: Optional[float],
    limit: int = 3
) -> List[Product]:
    results = [p for p in items if not _is_noise_name(p.name)]

    if max_price is not None:
        results = [p for p in results if p.price <= max_price]

    if not keyword:
        ranked = sorted(
            results,
            key=lambda p: (_is_tiny_or_sample(p.name), p.price, p.name.lower())
        )
        return ranked[:limit]

    scored = []
    for p in results:
        s = _score_product(p.name, keyword)
        if s >= 18:
            scored.append((s, p))

    if not scored:
        return []

    scored.sort(
        key=lambda x: (
            -x[0],
            _is_tiny_or_sample(x[1].name),
            x[1].price,
            x[1].name.lower()
        )
    )

    chosen = []
    seen = set()
    for _, p in scored:
        key = _normalize(p.name)
        if key in seen:
            continue
        seen.add(key)
        chosen.append(p)
        if len(chosen) >= limit:
            break

    return chosen