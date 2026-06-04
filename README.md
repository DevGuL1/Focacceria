# Focacceria Django CMS

Born in Italy, Baked in Tbilisi 🇮🇹

## სწრაფი დაწყება

```bash
# 1. Dependencies
pip install -r requirements.txt

# 2. Database
python manage.py migrate

# 3. Initial Data
python manage.py seed_data

# 4. Superuser
python manage.py createsuperuser

# 5. Run
python manage.py runserver
```

## შესვლა

| URL | აღწერა |
|-----|--------|
| http://127.0.0.1:8000/ | საიტი |
| http://127.0.0.1:8000/dashboard/ | Admin Dashboard |
| http://127.0.0.1:8000/dashboard/login/ | Login |

**Default credentials:** `admin` / `focacceria2024`

## Dashboard ფუნქციები

- ⚙ **საიტის პარამეტრები** — ლოგო, კონტაქტი, About
- ▶ **სლაიდერები** — Hero სლაიდების მართვა
- ☰ **ნავიგაცია** — Drag & Drop თანმიმდევრობა
- ▤ **Footer** — სვეტები და ბმულები
- 🔍 **SEO** — Title, Description, OG Image
- 📂 **კატეგორიები** — Menu / Salumeria კატეგ.
- 🍽 **პროდუქტები** — ფასები, სურათები, Drag & Drop
- ➕ **Add-ons** — დამატებითი ინგრედიენტები
- 🌐 **ენები** — ქართული / English toggle

## ბრენდინგი

- **Primary:** #C8102E (Rosso)
- **Dark:** #1A1210 (Nero)
- **Cream:** #F5EFE0 (Crema)
- **Gold:** #C4A052 (Oro)
- **Fonts:** Playfair Display + Inter
