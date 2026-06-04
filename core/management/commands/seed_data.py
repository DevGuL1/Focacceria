from django.core.management.base import BaseCommand
from core.models import SiteSettings, NavigationItem, FooterColumn, FooterLink, SEOSettings
from menu.models import MenuCategory, MenuItem


class Command(BaseCommand):
    help = 'Seed initial Focacceria data'

    def handle(self, *args, **options):
        self.stdout.write('🍕 Seeding Focacceria data...')

        # Site Settings
        s = SiteSettings.get_settings()
        s.tagline_ka = 'დაბადებული იტალიაში, გამომცხვარი თბილისში'
        s.tagline_en = 'Born in Italy, Baked in Tbilisi'
        s.phone = '+995 598 80 00 45'
        s.address_ka = 'თბილისი, ძველი ქალაქი'
        s.address_en = 'Tbilisi, Old Town'
        s.opening_hours_ka = 'ორშ–პარ: 11:00–22:00\nშაბ–კვი: 10:00–23:00'
        s.opening_hours_en = 'Mon–Fri: 11:00–22:00\nSat–Sun: 10:00–23:00'
        s.instagram = 'https://instagram.com/focacceria.ge'
        s.whatsapp = '995598800045'
        s.about_title_ka = 'ჩვენს შესახებ'
        s.about_title_en = 'About Us'
        s.about_text_ka = 'Georgia-ს პირველი და ერთადერთი სქიაჩატას სენდვიჩების მაღაზია. ყველა ინგრედიენტი პირდაპირ იტალიიდან — ფქვილი, დუღილის კულტურები, ხორცეული და ყველი.'
        s.about_text_en = "Georgia's first and only Schiacciata sandwich shop. All ingredients sourced directly from Italy — flour, fermentation cultures, charcuterie and cheese."
        s.save()

        # Navigation
        if not NavigationItem.objects.exists():
            nav_items = [
                ('მთავარი', 'Home', '/'),
                ('მენიუ', 'Menu', '/menu/'),
                ('სალუმერია', 'Salumeria', '/salumeria/'),
            ]
            for i, (ka, en, url) in enumerate(nav_items):
                NavigationItem.objects.create(label_ka=ka, label_en=en, url=url, order=i)
            self.stdout.write('  ✓ Navigation items created')

        # Footer
        if not FooterColumn.objects.exists():
            col1 = FooterColumn.objects.create(title_ka='მენიუ', title_en='Menu', order=0)
            FooterLink.objects.create(column=col1, label_ka='მენიუ', label_en='Menu', url='/menu/', order=0)
            FooterLink.objects.create(column=col1, label_ka='სალუმერია', label_en='Salumeria', url='/salumeria/', order=1)

            col2 = FooterColumn.objects.create(title_ka='შეკვეთა', title_en='Order', order=1)
            FooterLink.objects.create(column=col2, label_ka='Wolt', label_en='Wolt', url='#', order=0, open_new_tab=True)
            FooterLink.objects.create(column=col2, label_ka='Glovo', label_en='Glovo', url='#', order=1, open_new_tab=True)

            col3 = FooterColumn.objects.create(title_ka='კონტაქტი', title_en='Contact', order=2)
            FooterLink.objects.create(column=col3, label_ka='+995 598 80 00 45', label_en='+995 598 80 00 45', url='tel:+995598800045', order=0)
            FooterLink.objects.create(column=col3, label_ka='Instagram', label_en='Instagram', url='https://instagram.com/focacceria.ge', order=1, open_new_tab=True)
            self.stdout.write('  ✓ Footer columns & links created')

        # SEO
        seo_defaults = {
            'home': {
                'title_ka': 'Focacceria — დაბადებული იტალიაში, გამომცხვარი თბილისში',
                'title_en': 'Focacceria — Born in Italy, Baked in Tbilisi',
                'description_ka': 'Georgia-ს პირველი სქიაჩატას სენდვიჩების მაღაზია თბილისში. 100% იტალიური ინგრედიენტები.',
                'description_en': "Georgia's first Schiacciata sandwich shop in Tbilisi. 100% Italian ingredients.",
            },
            'menu': {
                'title_ka': 'მენიუ — Focacceria Tbilisi',
                'title_en': 'Menu — Focacceria Tbilisi',
                'description_ka': 'ავთენტური სქიაჩატას სენდვიჩები — მორტადელა, პროშუტო, სალსიჩა და სხვა.',
                'description_en': 'Authentic Schiacciata sandwiches — Mortadella, Prosciutto, Salsiccia and more.',
            },
            'salumeria': {
                'title_ka': 'სალუმერია — Focacceria Tbilisi',
                'title_en': 'Salumeria — Focacceria Tbilisi',
                'description_ka': 'იტალიური ხორცეული და ყველი — Leoncini, Simonini. მხოლოდ თბილისში.',
                'description_en': 'Italian cured meats & cheeses — Leoncini, Simonini. Only in Tbilisi.',
            },
        }
        for page, defaults in seo_defaults.items():
            obj, created = SEOSettings.objects.get_or_create(page=page)
            if created:
                for k, v in defaults.items():
                    setattr(obj, k, v)
                obj.save()
        self.stdout.write('  ✓ SEO settings created')

        # Menu Categories & Items
        if not MenuCategory.objects.exists():
            categories = [
                ('მორტადელა', 'Mortadella', 'mortadella', 'menu', [
                    ('მორტაცა კლასიკა', 'Mortadella Classica', 'მორტადელა, პარმეზანის კრემი, პომიდორი, არტიშოკი, მწვანე პესტო', 'Mortadella, Parmesan Cream, Tomato, Artichoke, Green Pesto', 27),
                    ('მორტაცა ფრესკა', 'Mortazza Fresca', 'მორტადელა, სტრაჩიატელა, პომიდორი, კრემ-პესტო, ბაზილიკო', 'Mortadella, Stracciatella, Tomato, Cream Pesto, Basil', 28),
                    ('მორტაცა როსა', 'Mortazza Rossa', 'მორტადელა, სტრაჩიატელა, პომიდორი, მზეში გამხმარი პომიდორი, წითელი პესტო', 'Mortadella, Stracciatella, Tomato, Sun-dried Tomatoes, Red Pesto', 28, True),
                    ('ლა პარადიზო', 'La Paradiso', 'მორტადელა, სტრაჩიატელა, დაფქული ფისტა, კრემ-პესტო, ბაზილიკო', 'Mortadella, Stracciatella, Crushed Pistachio, Cream Pesto, Basil', 29),
                    ('ბოლონია ტარტუფო', 'Bologna Tartufo', 'მორტადელა, სტრაჩიატელა, ტრიუფელის კრემი, არუგულა', 'Mortadella, Stracciatella, Truffle Cream, Arugula', 31),
                ]),
                ('პროშუტო', 'Prosciutto', 'prosciutto', 'menu', [
                    ('ლა პრიმავერა', 'La Primavera', 'პროშუტო კოტო, სტრაჩიატელა, გარგარი, ბაზილიკო', 'Prosciutto Cotto, Stracciatella, Apricot, Basil', 28),
                    ('ანტიკო როსო', 'Antico Rosso', 'პროშუტო კოტო, სტრაჩიატელა, წითელი პესტო', 'Prosciutto Cotto, Stracciatella, Red Pesto', 29),
                    ('პროშუტო დოლჩე სალატო', 'Prosciutto Dolce Salato', 'პროშუტო კრუდო, სტრაჩიატელა, პომიდორი', 'Prosciutto Crudo, Stracciatella, Tomato', 29),
                    ('დოლჩე პიკანტე', 'Dolce Piccante', 'პროშუტო კრუდო, სტრაჩიატელა, ნდუია', 'Prosciutto Crudo, Stracciatella, Nduja', 31),
                    ('პროშუტო როიალე', 'Prosciutto Royale', 'პროშუტო დი პარმა, სტრაჩიატელა, ბაზილიკო', 'Prosciutto di Parma, Stracciatella, Basil', 33, True),
                ]),
                ('მილანო & სალსიჩა', 'Milano & Salsiccia', 'milano-salsiccia', 'menu', [
                    ('მილანო კლასიკო', 'Milano Classico', 'მილანეზე სალამი, სტრაჩიატელა, პომიდორი', 'Milano Salami, Stracciatella, Tomato', 28),
                    ('სალსიჩა ვერდე', 'Salsiccia Verde', 'ახალი სალსიჩა, სტრაჩიატელა, პესტო', 'Fresh Salsiccia, Stracciatella, Pesto', 29),
                    ('სალსიჩა რუსტიკა', 'Salsiccia Rustica', 'სალსიჩა, სტრაჩიატელა, ბრასიკა', 'Salsiccia, Stracciatella, Brassica', 31, True),
                ]),
                ('ვეგეტარიანული & ვეგანური', 'Vegetarian & Vegan', 'vegetarian-vegan', 'menu', [
                    ('ბრუსკეტა ვერდე', 'Bruschetta Verde', 'ავოკადო, სტრაჩიატელა, ლიმონი, ბაზილიკო', 'Avocado, Stracciatella, Lemon, Basil', 22),
                    ('კაპრეზე კლასიკო', 'Caprese Classico', 'ფლოტ დი ლატე, პომიდორი, ბაზილიკო, ზეთი', 'Fior di Latte, Tomato, Basil, Olive Oil', 25),
                    ('კაპრეზე ვერდე', 'Caprese Verde', 'სტრაჩიატელა, პესტო, არუგულა, კედრის კაკალი', 'Stracciatella, Pesto, Arugula, Pine Nuts', 27, True),
                    ('ბელა ვეგანა', 'Bella Vegana', 'ავოკადო, მზეში გამხმარი პომიდორი, პესტო', 'Avocado, Sun-dried Tomato, Vegan Pesto', 29),
                ]),
                ('სალათები ფოკაჩიასთან', 'Salads with Focaccia', 'salads', 'menu', [
                    ('სალათა ნიჩოიზე', 'Salade Niçoise', 'ტუნა, კვერცხი, ზეითონი, პომიდორი', 'Tuna, Egg, Olives, Tomato', 27),
                    ('ბუფალო სალათა', 'Buffalo Salad', 'ბუფალოს მოცარელა, პომიდორი, ბაზილიკო', 'Buffalo Mozzarella, Tomato, Basil', 28),
                    ('სეზარი ფოკაჩიასთან', 'Caesar with Focaccia', 'ქათამი, პარმეზანი, სეზარის სოუსი', 'Chicken, Parmesan, Caesar Dressing', 30),
                ]),
                ('ტკბილეული', 'Sweets', 'sweets', 'menu', [
                    ('ნუტელა & ნოჩოლა', 'Nutella & Nocciola', 'ნუტელა, დაფქული თხილი', 'Nutella, Crushed Hazelnuts', 15),
                    ('ტირამისუ', 'Tiramisu', 'კლასიკური ტირამისუ', 'Classic Tiramisu', 13),
                    ('პანა კოტა', 'Panna Cotta', 'ვანილის პანა კოტა', 'Vanilla Panna Cotta', 12),
                ]),
            ]

            for cat_ka, cat_en, slug, page, items_data in categories:
                cat = MenuCategory.objects.create(
                    name_ka=cat_ka, name_en=cat_en, slug=slug, page=page,
                    order=MenuCategory.objects.count()
                )
                for j, item_data in enumerate(items_data):
                    is_featured = item_data[4] if len(item_data) > 4 else False
                    MenuItem.objects.create(
                        category=cat,
                        name_ka=item_data[0], name_en=item_data[1],
                        description_ka=item_data[2], description_en=item_data[3],
                        price=item_data[4],
                        is_featured=len(item_data) > 5 and bool(item_data[5]),
                        order=j,
                    )

            self.stdout.write('  ✓ Menu categories & items created')

        # Salumeria
        if not MenuCategory.objects.filter(page='salumeria').exists():
            sal_cats = [
                ('სალუმი', 'Salumi', 'salumi', [
                    ('მორტადელა ბოლონეზე', 'Mortadella Bolognese', 'Leoncini 1918 — DOP', 'Leoncini 1918 — DOP certified', 8.5, '100g'),
                    ('სალამი მილანო', 'Salami Milano', 'Simonini — BIO/IFS', 'Simonini — BIO/IFS certified', 9, '100g'),
                    ('პროშუტო კოტო', 'Prosciutto Cotto', 'Simonini — Slow Food', 'Simonini — Slow Food', 9.5, '100g'),
                    ('პროშუტო კრუდო', 'Prosciutto Crudo', 'DOP — 18 თვე', 'DOP — 18 months aged', 11, '100g'),
                    ('ნდუია', 'Nduja', 'კალაბრიური ცხარე სალამი', 'Calabrian spicy salami spread', 10, '100g'),
                    ('სალსიჩა სეკა', 'Salsiccia Secca', 'გამხმარი სალსიჩა', 'Dried Salsiccia', 10.5, '100g'),
                ]),
                ('ფორმაჯი', 'Formaggi', 'formaggi', [
                    ('სტრაჩიატელა', 'Stracciatella', '48 სთ-ით ადრე შეკვეთა', '48h pre-order required', 12, '100g'),
                    ('მოცარელა ფლოტ დი ლატე', 'Mozzarella Fior di Latte', '48 სთ-ით ადრე შეკვეთა', '48h pre-order required', 10, '100g'),
                    ('პარმიჯანო რეჯანო', 'Parmigiano Reggiano', 'DOP — 24 თვე', 'DOP — 24 months aged', 14, '100g'),
                ]),
                ('ჯელატო', 'Gelato Artigianale', 'gelato', [
                    ('პისტაჩო', 'Pistacchio', 'სიჩილიური ფისტა', 'Sicilian pistachio', 8, 'portion'),
                    ('ფლოტ დი ლატე', 'Fior di Latte', 'კლასიკური', 'Classic cream', 8, 'portion'),
                    ('ფრაგოლა', 'Fragola', 'მარწყვი', 'Strawberry', 8, 'portion'),
                ]),
            ]

            for cat_ka, cat_en, slug, items_data in sal_cats:
                cat = MenuCategory.objects.create(
                    name_ka=cat_ka, name_en=cat_en, slug=f'sal-{slug}', page='salumeria',
                    order=MenuCategory.objects.count()
                )
                for j, item_data in enumerate(items_data):
                    MenuItem.objects.create(
                        category=cat,
                        name_ka=item_data[0], name_en=item_data[1],
                        description_ka=item_data[2], description_en=item_data[3],
                        price=item_data[4], price_unit=item_data[5],
                        order=j,
                    )
            self.stdout.write('  ✓ Salumeria categories & items created')

        self.stdout.write(self.style.SUCCESS('\n✅ Focacceria data seeded successfully!'))
