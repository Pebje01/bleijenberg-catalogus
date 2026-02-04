#!/usr/bin/env python3
"""Convert all images to WebP format"""

import os
from PIL import Image
import glob

# Vind alle PNG, JPG, JPEG bestanden
image_files = glob.glob('*.png') + glob.glob('*.PNG') + glob.glob('*.jpg') + glob.glob('*.jpeg') + glob.glob('*.JPG') + glob.glob('*.JPEG')

print(f"Gevonden {len(image_files)} afbeeldingen om te converteren\n")

conversions = []

for image_file in image_files:
    try:
        # Open afbeelding
        img = Image.open(image_file)

        # Converteer RGBA naar RGB als nodig
        if img.mode == 'RGBA':
            # Maak witte achtergrond
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # Alpha channel als mask
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Nieuwe bestandsnaam (behoud originele naam maar verander extensie)
        base_name = os.path.splitext(image_file)[0]
        webp_file = f"{base_name}.webp"

        # Sla op als WebP met hoge kwaliteit
        img.save(webp_file, 'WEBP', quality=85, method=6)

        # Haal bestandsgroottes op
        original_size = os.path.getsize(image_file)
        webp_size = os.path.getsize(webp_file)
        reduction = ((original_size - webp_size) / original_size) * 100

        print(f"✓ {image_file}")
        print(f"  → {webp_file}")
        print(f"  {original_size:,} bytes → {webp_size:,} bytes (-{reduction:.1f}%)\n")

        conversions.append({
            'original': image_file,
            'webp': webp_file,
            'reduction': reduction
        })

        # Verwijder origineel bestand
        os.remove(image_file)
        print(f"  🗑️  Origineel verwijderd\n")

    except Exception as e:
        print(f"✗ Fout bij {image_file}: {e}\n")

print(f"\n{'='*60}")
print(f"Conversie compleet!")
print(f"  {len(conversions)} afbeeldingen geconverteerd naar WebP")
print(f"  Originele bestanden verwijderd")

# Bereken totale besparing
if conversions:
    avg_reduction = sum(c['reduction'] for c in conversions) / len(conversions)
    print(f"  Gemiddelde bestandsgrootte reductie: {avg_reduction:.1f}%")
