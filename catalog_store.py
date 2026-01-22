import json
from dataclasses import dataclass
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
        # aceita campos extras se existirem
        name = it.get("name")
        price = it.get("price")
        url = it.get("url")
        if name and (price is not None) and url:
            items.append(Product(name=name, price=float(price), url=url))
    return items

def search_catalog(items: List[Product], keyword: Optional[str], max_price: Optional[float], limit: int = 3) -> List[Product]:
    results = items

    if max_price is not None:
        results = [p for p in results if p.price <= max_price]

    if keyword:
        kw = keyword.lower().strip()
        def score(p: Product) -> int:
            return p.name.lower().count(kw)
        results = sorted(results, key=score, reverse=True)
        # se nada casa, ordena por preço
        if results and score(results[0]) == 0:
            results = sorted(results, key=lambda p: p.price)
    else:
        results = sorted(results, key=lambda p: p.price)

    return results[:limit]
