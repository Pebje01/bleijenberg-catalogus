#!/usr/bin/env python3
"""Update catalogus with Bleijenberg color scheme"""

import json

# Lees gefilterde producten
with open('products_filtered.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Converteer naar JavaScript array
products_js = json.dumps(products, ensure_ascii=False)

html_template = f'''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bleijenberg Catalogus</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #E8DCC4 0%, #D4C4A8 100%);
            min-height: 100vh;
            padding: 20px;
            position: relative;
        }}

        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('Noise Seamless Vector Patterns copy.webp') repeat;
            background-size: 100px 100px;
            opacity: 0.5;
            pointer-events: none;
            z-index: 0;
        }}

        /* Login scherm */
        #login-screen {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('BB-logo-achtergrond.webp') center/cover no-repeat;
            z-index: 1000;
        }}

        #login-screen::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.3);
            z-index: -1;
        }}

        .login-box {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
            width: 100%;
            max-width: 400px;
            border: 2px solid #D4C4A8;
            position: relative;
            z-index: 10;
        }}

        .login-box h1 {{
            color: #7A5022;
            margin-bottom: 30px;
            text-align: center;
            font-size: 28px;
        }}

        .login-box input {{
            width: 100%;
            padding: 15px;
            margin-bottom: 20px;
            border: 2px solid #D4C4A8;
            border-radius: 8px;
            font-size: 16px;
        }}

        .login-box input:focus {{
            outline: none;
            border-color: #7A5022;
        }}

        .login-box button {{
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #7A5022 0%, #5D3C1A 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .login-box button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(122, 80, 34, 0.3);
        }}

        .error-message {{
            color: #BE010d;
            text-align: center;
            margin-top: 10px;
            display: none;
        }}

        /* Catalogus */
        #catalogus {{
            display: none;
            max-width: 1400px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }}

        header {{
            background: white;
            padding: 20px 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 20px rgba(122, 80, 34, 0.15);
            border-top: 4px solid #7A5022;
        }}

        h1 {{
            color: #000000;
            margin-bottom: 20px;
            font-size: 32px;
        }}

        .controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            align-items: center;
            margin-bottom: 20px;
        }}

        .search-box {{
            flex: 1;
            min-width: 200px;
        }}

        .search-box input {{
            width: 100%;
            padding: 12px 20px;
            border: 2px solid #D4C4A8;
            border-radius: 8px;
            font-size: 16px;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: #7A5022;
        }}

        .btw-toggle {{
            display: flex;
            background: white;
            border: 2px solid #D4C4A8;
            border-radius: 8px;
            overflow: hidden;
        }}

        .btw-toggle button {{
            padding: 12px 20px;
            border: none;
            background: transparent;
            color: #5D3C1A;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .btw-toggle button.active {{
            background: #7A5022;
            color: white;
        }}

        .btw-toggle button:hover:not(.active) {{
            background: #F5F0E8;
        }}

        .logout-btn {{
            padding: 12px 24px;
            background: #5D3C1A;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, background 0.2s;
        }}

        .logout-btn:hover {{
            transform: translateY(-2px);
            background: #7A5022;
        }}

        .btw-label {{
            font-size: 12px;
            color: #999;
            margin-left: 5px;
        }}

        .stats {{
            display: flex;
            gap: 20px;
            padding: 15px;
            background: #F5F0E8;
            border-radius: 8px;
            border-left: 4px solid #7A5022;
        }}

        .stat-item {{
            font-size: 14px;
            color: #333333;
        }}

        .stat-item strong {{
            color: #000000;
            font-size: 18px;
        }}

        .product-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
        }}

        .product-card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(122, 80, 34, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            border: 1px solid #E8DCC4;
        }}

        .product-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(122, 80, 34, 0.2);
            border-color: #7A5022;
        }}

        .product-image {{
            width: 100%;
            height: 250px;
            object-fit: cover;
            cursor: pointer;
            background: #F5F0E8;
        }}

        .product-info {{
            padding: 20px;
        }}

        .product-title {{
            font-size: 18px;
            font-weight: 600;
            color: #000000;
            margin-bottom: 10px;
            line-height: 1.4;
        }}

        .product-sku {{
            font-size: 12px;
            color: #9B8B6F;
            margin-bottom: 10px;
            font-family: monospace;
            background: #F5F0E8;
            padding: 4px 8px;
            border-radius: 4px;
            display: inline-block;
        }}

        .product-price {{
            font-size: 24px;
            font-weight: 700;
            color: #7A5022;
            margin-bottom: 10px;
        }}

        .product-dimensions {{
            color: #333333;
            margin-bottom: 10px;
            font-size: 14px;
        }}

        .product-description {{
            color: #333333;
            font-size: 14px;
            margin-top: 10px;
            line-height: 1.5;
        }}

        .product-link {{
            display: inline-block;
            margin-top: 10px;
            color: #7A5022;
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
            transition: color 0.2s;
        }}

        .product-link:hover {{
            color: #5D3C1A;
            text-decoration: underline;
        }}

        /* Lightbox voor afbeeldingen */
        #lightbox {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(93, 60, 26, 0.95);
            z-index: 2000;
            justify-content: center;
            align-items: center;
        }}

        #lightbox img {{
            max-width: 90%;
            max-height: 90%;
            border-radius: 10px;
            box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
        }}

        #lightbox .close {{
            position: absolute;
            top: 30px;
            right: 30px;
            color: white;
            font-size: 40px;
            cursor: pointer;
            background: rgba(122, 80, 34, 0.8);
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s;
        }}

        #lightbox .close:hover {{
            background: rgba(122, 80, 34, 1);
        }}

        .no-results {{
            text-align: center;
            padding: 60px;
            background: white;
            border-radius: 15px;
            color: #333333;
            border: 2px dashed #D4C4A8;
        }}

        @media (max-width: 768px) {{
            .controls {{
                flex-direction: column;
                align-items: stretch;
            }}

            .product-grid {{
                grid-template-columns: 1fr;
            }}

            h1 {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <!-- Login Scherm -->
    <div id="login-screen">
        <div class="login-box">
            <h1>Bleijenberg Catalogus</h1>
            <input type="password" id="password-input" placeholder="Voer wachtwoord in" />
            <button onclick="checkPassword()">Inloggen</button>
            <div class="error-message" id="error-message">Onjuist wachtwoord</div>
        </div>
    </div>

    <!-- Catalogus -->
    <div id="catalogus">
        <header>
            <h1>Bleijenberg Productcatalogus</h1>

            <div class="controls">
                <div class="search-box">
                    <input type="text" id="search" placeholder="Zoek op titel, SKU of maten..." oninput="filterProducts()" />
                </div>

                <div class="btw-toggle">
                    <button class="active" onclick="toggleBTW(true)">Incl. BTW</button>
                    <button onclick="toggleBTW(false)">Excl. BTW</button>
                </div>

                <button class="logout-btn" onclick="logout()">Uitloggen</button>
            </div>

            <div class="stats">
                <div class="stat-item"><strong id="product-count">0</strong> producten</div>
                <div class="stat-item"><strong id="visible-count">0</strong> zichtbaar</div>
            </div>
        </header>

        <div class="product-grid" id="product-grid"></div>

        <div class="no-results" id="no-results" style="display: none;">
            Geen producten gevonden
        </div>
    </div>

    <!-- Lightbox -->
    <div id="lightbox" onclick="closeLightbox()">
        <span class="close">&times;</span>
        <img id="lightbox-img" src="" alt="">
    </div>

    <script>
        const PASSWORD = 'potten01';
        const BTW_PERCENTAGE = 0.21; // 21% BTW
        let showInclBTW = true;

        // Productdata direct embedded
        const productsData = {products_js};

        // Login functie
        function checkPassword() {{
            const input = document.getElementById('password-input').value;
            if (input === PASSWORD) {{
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('catalogus').style.display = 'block';
                displayProducts(productsData);
                updateStats();
            }} else {{
                document.getElementById('error-message').style.display = 'block';
            }}
        }}

        // Enter key support voor login
        document.getElementById('password-input')?.addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                checkPassword();
            }}
        }});

        // Logout
        function logout() {{
            document.getElementById('login-screen').style.display = 'flex';
            document.getElementById('catalogus').style.display = 'none';
            document.getElementById('password-input').value = '';
            document.getElementById('error-message').style.display = 'none';
        }}

        // BTW toggle functie
        function toggleBTW(inclBTW) {{
            showInclBTW = inclBTW;

            // Update active state buttons
            const buttons = document.querySelectorAll('.btw-toggle button');
            buttons.forEach((btn, index) => {{
                if ((index === 0 && inclBTW) || (index === 1 && !inclBTW)) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});

            // Re-render products met nieuwe prijzen
            filterProducts();
        }}

        // Bereken prijs op basis van BTW setting (met 30% inkoopkorting)
        function calculatePrice(priceString) {{
            const price = parseFloat(priceString.replace('€', '').replace(',', '.'));
            if (isNaN(price)) return priceString;

            // Pas 30% inkoopkorting toe
            const inkoopPrice = price * 0.7;

            if (showInclBTW) {{
                return `€${{inkoopPrice.toFixed(2)}} <span class="btw-label">(incl. BTW)</span>`;
            }} else {{
                const exclPrice = inkoopPrice / (1 + BTW_PERCENTAGE);
                return `€${{exclPrice.toFixed(2)}} <span class="btw-label">(excl. BTW)</span>`;
            }}
        }}

        // Toon producten
        function displayProducts(products) {{
            const grid = document.getElementById('product-grid');
            const noResults = document.getElementById('no-results');

            if (products.length === 0) {{
                grid.innerHTML = '';
                noResults.style.display = 'block';
                return;
            }}

            noResults.style.display = 'none';

            grid.innerHTML = products.map(product => {{
                return `
                    <div class="product-card">
                        <img src="${{product.images[0] || 'placeholder.jpg'}}"
                             alt="${{product.title}}"
                             class="product-image"
                             onclick="openLightbox('${{product.images[0]}}')"
                             onerror="this.src='https://via.placeholder.com/300x250?text=Geen+afbeelding'">

                        <div class="product-info">
                            <div class="product-title">${{product.title}}</div>
                            ${{product.sku ? `<div class="product-sku">SKU: ${{product.sku}}</div>` : ''}}

                            <div class="product-price">${{calculatePrice(product.price)}}</div>

                            ${{product.dimensions ? `<div class="product-dimensions">📏 ${{product.dimensions}} cm</div>` : ''}}

                            ${{product.description ? `<div class="product-description">${{product.description.substring(0, 150)}}${{product.description.length > 150 ? '...' : ''}}</div>` : ''}}

                            <a href="${{product.url}}" target="_blank" class="product-link">Bekijk op website →</a>
                        </div>
                    </div>
                `;
            }}).join('');

            updateStats(products.length);
        }}

        // Filter producten
        function filterProducts() {{
            const searchTerm = document.getElementById('search').value.toLowerCase();

            const filtered = productsData.filter(product => {{
                return product.title.toLowerCase().includes(searchTerm) ||
                       product.description.toLowerCase().includes(searchTerm) ||
                       product.sku.toLowerCase().includes(searchTerm) ||
                       product.dimensions.toLowerCase().includes(searchTerm);
            }});

            displayProducts(filtered);
        }}

        // Update statistieken
        function updateStats(visibleCount = null) {{
            document.getElementById('product-count').textContent = productsData.length;
            document.getElementById('visible-count').textContent = visibleCount !== null ? visibleCount : productsData.length;
        }}

        // Lightbox functies
        function openLightbox(imageSrc) {{
            document.getElementById('lightbox').style.display = 'flex';
            document.getElementById('lightbox-img').src = imageSrc;
        }}

        function closeLightbox() {{
            document.getElementById('lightbox').style.display = 'none';
        }}

        // ESC key voor lightbox sluiten
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{
                closeLightbox();
            }}
        }});
    </script>
</body>
</html>'''

# Schrijf naar catalogus.html
with open('catalogus.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('✓ Catalogus bijgewerkt met Bleijenberg kleuren!')
print('  Kleurenschema:')
print('  - Hoofdkleur: #7A5022 (bruin)')
print('  - Achtergrond: #E8DCC4 (beige)')
print('  - Donker: #5D3C1A (donkerbruin)')
print('  - Accenten: #D4C4A8 (zand)')
