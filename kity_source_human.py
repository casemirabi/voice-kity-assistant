import re, json
from dataclasses import dataclass, asdict
from typing import List, Optional
from playwright.sync_api import sync_playwright

BASE_URL = "https://seame0501.kyte.site/pt-BR"
CACHE_PATH = "catalog_cache.json"
USER_DATA_DIR = "pw_profile"  # pasta com cookies/sessão

@dataclass
class Product:
    name: str
    price: Optional[float]
    url: str

_price_re = re.compile(r"R\$\s*([\d\.]+,\d{2})", re.I)

def _parse_price(text: str) -> Optional[float]:
    m = _price_re.search(text.replace("\xa0", " "))
    if not m: return None
    return float(m.group(1).replace(".", "").replace(",", "."))

def save_cache(items: List[Product]):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump([asdict(x) for x in items], f, ensure_ascii=False, indent=2)

def fetch_after_human_check(headless: bool) -> List[Product]:
    with sync_playwright() as p:
        # contexto persistente = guarda cookies/sessão
        ctx = p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=headless,
            viewport={"width": 1280, "height": 800},
        )
        page = ctx.new_page()
        page.goto(BASE_URL, wait_until="domcontentloaded", timeout=120000)

        if not headless:
            print("\n✅ Se aparecer 'Just a moment', resolva no navegador.")
            print("Quando a HOME carregar com os produtos, volte aqui e aperte ENTER.\n")
            input()

        # tenta coletar cards (quando a página REAL carregar)
        page.wait_for_timeout(2000)

        raw = page.evaluate("""
            () => {
              const cards = document.querySelectorAll("[data-testid^='card-product-']");
              return Array.from(cards).map(card => {
                const nameEl = card.querySelector("[data-testid='name-product-home']");
                const priceEl = card.querySelector("[data-testid='price-product-home']");
                const linkEl = card.querySelector("a[href*='/pt-BR/p/']");
                return {
                  name: nameEl?.innerText?.trim() || null,
                  price: priceEl?.innerText?.trim() || null,
                  url: linkEl?.href || null
                };
              });
            }
        """)

        ctx.close()

    items: List[Product] = []
    for it in raw:
        if not it["name"] or not it["price"] or not it["url"]:
            continue
        price = _parse_price(it["price"])
        if price is None:
            continue
        items.append(Product(name=it["name"], price=price, url=it["url"]))
    return items

if __name__ == "__main__":
    # 1) primeira vez: abre visível pra você passar no Cloudflare manualmente
    items = fetch_after_human_check(headless=False)
    print("Coletados (visível):", len(items))
    save_cache(items)

    # 2) tentativa headless reaproveitando o perfil (pode funcionar dependendo da política do Cloudflare)
    items2 = fetch_after_human_check(headless=True)
    print("Coletados (headless):", len(items2))
    save_cache(items2 if items2 else items)
    print("Cache salvo em", CACHE_PATH)
