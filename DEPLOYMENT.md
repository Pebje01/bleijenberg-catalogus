# Deployment Instructies

## 🎉 Catalogus is klaar!

### Wat is er gemaakt:
- ✅ 28 producten met afbeeldingen, prijzen, SKU's
- ✅ Wachtwoordbeveiliging (wachtwoord: `potten01`)
- ✅ 20% inkoopkorting automatisch toegepast
- ✅ Incl./Excl. BTW schakelaar (default: excl.)
- ✅ 2 gereserveerde producten (CLP00006, CLP00007)
- ✅ Bleijenberg kleuren en branding
- ✅ WebP afbeeldingen (78% kleiner)
- ✅ Responsive design

**Totale cataloguswaarde:** €7.911,40 excl. BTW

---

## 📤 Stap 1: Push naar GitHub

```bash
# 1. Maak een nieuwe repository op github.com
#    Ga naar: https://github.com/new
#    Naam: bleijenberg-catalogus
#    Type: Public of Private
#    NIET initialiseren met README

# 2. Push je code (vervang JOUW-USERNAME met je GitHub username)
cd "/Users/daleyjansen_1/Documents/Repos/Bleijenberg catalogus"
git remote add origin https://github.com/JOUW-USERNAME/bleijenberg-catalogus.git
git push -u origin main
```

---

## 🚀 Stap 2: Deploy op Vercel

### Optie A: Via Website (Makkelijkst)

1. Ga naar **https://vercel.com**
2. Klik **"Sign up"** of **"Log in"**
3. Klik **"Add New Project"**
4. Klik **"Import Git Repository"**
5. Selecteer **"bleijenberg-catalogus"**
6. Klik **"Deploy"** (zonder iets te wijzigen)

**Klaar!** Je catalogus is live op: `bleijenberg-catalogus.vercel.app`

### Optie B: Via Command Line

```bash
# Installeer Vercel CLI
npm install -g vercel

# Deploy
cd "/Users/daleyjansen_1/Documents/Repos/Bleijenberg catalogus"
vercel

# Follow de prompts:
# - Set up and deploy? Y
# - Which scope? (kies je account)
# - Link to existing project? N
# - Project name? bleijenberg-catalogus
# - In which directory? ./
# - Want to override settings? N
```

---

## 🔧 Na deployment

### Eigen domein toevoegen (optioneel)
1. Ga naar je Vercel project
2. Settings → Domains
3. Voeg toe: `catalogus.bleijenberg.eu`
4. Volg DNS instructies

### Automatische updates
Elke `git push` naar GitHub = automatische nieuwe deployment! 🎉

---

## 📝 Producten beheren

### Nieuwe producten toevoegen
```bash
cd "/Users/daleyjansen_1/Documents/Repos/Bleijenberg catalogus"
source venv/bin/activate
python3 scrape_products.py
python3 update_colors.py
git add -A
git commit -m "Update producten"
git push
```

### Product reserveren
Open `update_colors.py`, zoek naar:
```javascript
const RESERVED_SKUS = ['CLP00006', 'CLP00007'];
```
Voeg SKU toe, regenereer en push.

### Wachtwoord wijzigen
Open `update_colors.py`, zoek naar:
```javascript
const PASSWORD = 'potten01';
```
Wijzig, regenereer en push.

---

## 🆘 Hulp nodig?

- Vercel docs: https://vercel.com/docs
- GitHub hulp: https://docs.github.com
- Issues: Maak een issue aan in je repo
