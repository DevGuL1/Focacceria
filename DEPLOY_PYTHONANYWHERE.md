# 🚀 Focacceria — PythonAnywhere Deploy (უფასო)

სრულად უფასო, ბარათის გარეშე. SQLite ბაზა და ატვირთული სურათები **მუდმივად რჩება**.

---

## 1. ანგარიში
[www.pythonanywhere.com](https://www.pythonanywhere.com) → **Pricing & signup → Create a Beginner account** (უფასო).
დაიმახსოვრე შენი **username** (URL იქნება `username.pythonanywhere.com`).

## 2. კოდის ატვირთვა (Bash console)
Dashboard → **Consoles → Bash**. ჩაწერე (შეცვალე `YOURUSER` შენი username-ით):

```bash
git clone https://github.com/DevGuL1/Focacceria.git ~/Focacceria
python3.10 -m venv ~/.virtualenvs/focacceria
source ~/.virtualenvs/focacceria/bin/activate
cd ~/Focacceria
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --no-input
```

ან გაუშვი მზა სკრიპტი (ჯერ შეცვალე `YOURUSER` ფაილში):
```bash
bash ~/Focacceria/deploy/pythonanywhere_setup.sh
```

## 3. Web app შექმნა
Dashboard → **Web → Add a new web app** →
- **Manual configuration** (NOT "Django")
- **Python 3.10**

## 4. Virtualenv მითითება
Web tab → **Virtualenv** სექცია → ჩაწერე:
```
/home/YOURUSER/.virtualenvs/focacceria
```

## 5. WSGI ფაილი
Web tab → **Code** სექცია → დააჭირე WSGI ფაილის ბმულს →
წაშალე ყველაფერი და ჩასვი `deploy/pythonanywhere_wsgi.py`-ის შიგთავსი
(შეცვალე `YOURUSER` და `SECRET_KEY`). შეინახე.

## 6. Static & Media ფაილები
Web tab → **Static files** სექცია → დაამატე 2 ჩანაწერი:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOURUSER/Focacceria/staticfiles` |
| `/media/`  | `/home/YOURUSER/Focacceria/media` |

## 7. გაშვება
Web tab → ზემოთ მწვანე ღილაკი **Reload**.

✅ მზადაა: `https://YOURUSER.pythonanywhere.com/`

---

## შესვლა
| | |
|--|--|
| საიტი | `https://YOURUSER.pythonanywhere.com/` |
| Dashboard | `https://YOURUSER.pythonanywhere.com/dashboard/` |
| Admin | `admin` / `focacceria2024` |

dashboard-ში ცვლილებები და სურათები **მუდმივად ინახება** (რეალური დისკი).

---

## განახლება (კოდის შეცვლის შემდეგ)
```bash
cd ~/Focacceria && git pull
source ~/.virtualenvs/focacceria/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
```
შემდეგ Web tab → **Reload**.

## შენიშვნები
- უფასო ანგარიში „იძინებს" 3 თვეში თუ არ შეხვალ — უბრალოდ შედი და დააჭირე Reload.
- Tailwind/Google Fonts ბრაუზერში იტვირთება — PA-ის ქსელის შეზღუდვა არ გვეხება.
