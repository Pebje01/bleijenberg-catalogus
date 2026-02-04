#!/usr/bin/env python3
"""
Bleijenberg Product Scraper
Haalt alle productgegevens op van bleijenberg.eu
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re

# Lijst van alle product URLs
PRODUCT_URLS = [
    "https://bleijenberg.eu/product/beige-vintage-terra-kleien-vaas/",
    "https://bleijenberg.eu/product/test-product/",
    "https://bleijenberg.eu/product/mooie-beige-tinten-klei-vaas-57x57/",
    "https://bleijenberg.eu/product/mooie-terra-en-beige-vintage-klei-vaas/",
    "https://bleijenberg.eu/product/authentieke-vintage-vaas-terra-en-zand-kleur/",
    "https://bleijenberg.eu/product/vintage-grote-vaas-met-randen/",
    "https://bleijenberg.eu/product/vintage-kruik-met-ribbelstructuur/",
    "https://bleijenberg.eu/product/antieke-natuurstenen-trog-met-verweerde-patina/",
    "https://bleijenberg.eu/product/jumbo-natuurstenen-pot-beige-rond-47x85/",
    "https://bleijenberg.eu/product/beige-natuurstenen-jumbo-pot-met-patina-42x73/",
    "https://bleijenberg.eu/product/beige-natuurstenen-pot-met-lichte-patina-rond-42x73/",
    "https://bleijenberg.eu/product/grijze-antieke-jumbo-model-ronde-plantenpot-52x84/",
    "https://bleijenberg.eu/product/natuurstenen-pot-taps/",
    "https://bleijenberg.eu/product/natuurstenen-pot-beige-groot-rond/",
    "https://bleijenberg.eu/product/vintage-trog-mospatina-rechthoek/",
    "https://bleijenberg.eu/product/antieke-natuurstenen-trog-vierkant/",
    "https://bleijenberg.eu/product/natuurstenen-pot-licht-beige-rond/",
    "https://bleijenberg.eu/product/vintage-natuurstenen-trog-beige-vierkant/",
    "https://bleijenberg.eu/product/natuursteen-grote-pot-beige-rond/",
    "https://bleijenberg.eu/product/natuursteen-vintage-tog-vierkant/",
    "https://bleijenberg.eu/product/natuurstenen-grote-pot-beige-rond/",
    "https://bleijenberg.eu/product/natuursteen-pot-groot-rond/",
    "https://bleijenberg.eu/product/pot-6/",
    "https://bleijenberg.eu/product/natuurstenen-large-vintage-plantenpot-beige-grijs-rond/",
    "https://bleijenberg.eu/product/natuurstenen-pot-beige-rond/",
    "https://bleijenberg.eu/product/natuursteen-kleine-pot-unieke-afwerking-taps/",
    "https://bleijenberg.eu/product/natuurstenen-lichte-beige-pot-rechthoek/",
    "https://bleijenberg.eu/product/vintage-trog-klein-vierkant/",
    "https://bleijenberg.eu/product/natuursteen-pot-rond-grijs/",
]

def scrape_product(url):
    """Scrape een enkel product"""
    try:
        print(f"Scraping: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        product = {
            'url': url,
            'title': '',
            'price': '',
            'sku': '',
            'dimensions': '',
            'description': '',
            'images': [],
            'stock': ''
        }

        # Titel - gewoon <h1> zonder class
        title_elem = soup.find('h1')
        if title_elem:
            product['title'] = title_elem.get_text(strip=True)

        # SKU - zoek in span met 'sku' in class
        sku_elem = soup.find('span', class_=re.compile('sku', re.IGNORECASE))
        if sku_elem:
            sku_text = sku_elem.get_text(strip=True)
            # Verwijder "SKU" prefix als die er is
            sku_text = re.sub(r'^SKU\s*:?\s*', '', sku_text, flags=re.IGNORECASE)
            product['sku'] = sku_text

        # Prijs - probeer eerst JSON-LD, dan span
        json_ld = soup.find('script', type='application/ld+json')
        if json_ld:
            try:
                data = json.loads(json_ld.string)
                # Kan een lijst of enkel object zijn
                if isinstance(data, list):
                    for item in data:
                        if item.get('@type') == 'Product' and 'offers' in item:
                            price = item['offers'].get('price', '')
                            if price:
                                product['price'] = f"€{price}"
                                break
                elif data.get('@type') == 'Product' and 'offers' in data:
                    price = data['offers'].get('price', '')
                    if price:
                        product['price'] = f"€{price}"
            except:
                pass

        # Als JSON-LD niet werkt, probeer bdi elementen
        if not product['price'] or product['price'] == '€' or product['price'] == '€0.00':
            # Vind alle bdi elementen en neem de hoogste niet-nul prijs
            bdis = soup.find_all('bdi')
            for bdi in bdis:
                text = bdi.get_text(strip=True)
                if text and text != '€0.00' and '€' in text:
                    product['price'] = text
                    break

        # Afmetingen - zoek "Afmetingen (HxLxB):" in beschrijving
        desc = soup.find('div', class_='woocommerce-product-details__short-description')
        if desc:
            text = desc.get_text()
            # Zoek specifiek naar "Afmetingen (HxLxB): XX x XX x XX"
            dimension_match = re.search(r'Afmetingen[^:]*:\s*(\d+\s*[xX×]\s*\d+(?:\s*[xX×]\s*\d+)?)', text, re.IGNORECASE)
            if dimension_match:
                product['dimensions'] = dimension_match.group(1).strip()
            # Als niet gevonden, zoek algemeen patroon
            elif not product['dimensions']:
                dimension_match = re.search(r'(\d+)\s*[xX×]\s*(\d+)(?:\s*[xX×]\s*(\d+))?', text)
                if dimension_match:
                    product['dimensions'] = dimension_match.group(0)

        # Beschrijving
        desc_elem = soup.find('div', class_='woocommerce-product-details__short-description')
        if desc_elem:
            product['description'] = desc_elem.get_text(strip=True)

        # Voorraad - zoek in tekst naar "X in stock" of in availability class
        stock_text = soup.get_text()
        stock_match = re.search(r'(\d+)\s+in\s+stock', stock_text, re.IGNORECASE)
        if stock_match:
            product['stock'] = f"{stock_match.group(1)} op voorraad"
        else:
            # Probeer ook via class
            stock_elem = soup.find(class_=re.compile('stock|availability'))
            if stock_elem:
                product['stock'] = stock_elem.get_text(strip=True)

        # Afbeeldingen - verzamel alle galerij afbeeldingen
        gallery = soup.find('div', class_='woocommerce-product-gallery')
        if gallery:
            images = gallery.find_all('img')
            for img in images:
                src = img.get('src') or img.get('data-src')
                if src and src not in product['images']:
                    # Krijg de grote versie van de afbeelding
                    src = re.sub(r'-\d+x\d+\.', '.', src)
                    product['images'].append(src)

        # Als geen galerij, zoek hoofdafbeelding
        if not product['images']:
            main_img = soup.find('img', class_='wp-post-image')
            if main_img:
                src = main_img.get('src') or main_img.get('data-src')
                if src:
                    src = re.sub(r'-\d+x\d+\.', '.', src)
                    product['images'].append(src)

        return product

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main():
    """Scrape alle producten en sla op in JSON"""
    products = []

    for url in PRODUCT_URLS:
        product = scrape_product(url)
        if product:
            products.append(product)
        # Wees beleefd naar de server
        time.sleep(1)

    # Sla op in JSON bestand
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"\n✓ {len(products)} producten succesvol gescraped!")
    print(f"✓ Data opgeslagen in products.json")

if __name__ == '__main__':
    main()
