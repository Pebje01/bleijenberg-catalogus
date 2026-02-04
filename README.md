# Bleijenberg Productcatalogus

Wachtwoordbeveiligde webapp met alle Bleijenberg producten.

## Features

- 🔒 Wachtwoordbeveiliging (wachtwoord: `potten01`)
- 🎨 Bleijenberg kleuren en branding
- 📦 28 unieke producten met SKU's
- 🔍 Zoekfunctie (titel, SKU, afmetingen)
- 📱 Responsive design
- 🖼️ WebP afbeeldingen voor snelle laadtijd
- 🔗 Directe links naar productpagina's

## Gebruik

Open `catalogus.html` in je browser en log in met wachtwoord `potten01`.

## Producten bijwerken

Als er nieuwe producten zijn of prijzen zijn gewijzigd:

```bash
# Activeer virtual environment
source venv/bin/activate

# Scrape nieuwe productdata
python3 scrape_products.py

# Genereer nieuwe catalogus
python3 update_colors.py
```

## Wachtwoord wijzigen

Open `update_colors.py` en zoek naar:
```python
const PASSWORD = 'potten01';
```

Verander het wachtwoord en run:
```bash
python3 update_colors.py
```

## Deployment op Vercel

Deze app is klaar voor Vercel deployment. Zie instructies hieronder.
