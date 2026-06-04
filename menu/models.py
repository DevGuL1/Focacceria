from django.db import models


class MenuCategory(models.Model):
    PAGE_CHOICES = [
        ('menu', 'Menu'),
        ('salumeria', 'Salumeria'),
    ]
    name_ka = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description_ka = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    page = models.CharField(max_length=20, choices=PAGE_CHOICES, default='menu')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Menu Categories'

    def __str__(self):
        return self.name_en or self.name_ka

    def get_name(self, lang='ka'):
        return self.name_ka if lang == 'ka' else self.name_en


class MenuItem(models.Model):
    UNIT_CHOICES = [
        ('', 'ერთეული'),
        ('100g', '100 გრ'),
        ('portion', 'პორცია'),
    ]
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name_ka = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200)
    description_ka = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    price_unit = models.CharField(max_length=20, choices=UNIT_CHOICES, blank=True)
    image = models.ImageField(upload_to='menu/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags: vegan, vegetarian, spicy, new')
    badge_ka = models.CharField(max_length=50, blank=True, help_text='e.g. ახალი, ყველაზე პოპ.')
    badge_en = models.CharField(max_length=50, blank=True, help_text='e.g. New, Most Popular')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name_en or self.name_ka

    def get_name(self, lang='ka'):
        return self.name_ka if lang == 'ka' else self.name_en

    def get_description(self, lang='ka'):
        return self.description_ka if lang == 'ka' else self.description_en

    def get_badge(self, lang='ka'):
        return self.badge_ka if lang == 'ka' else self.badge_en

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class AddOn(models.Model):
    name_ka = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name_en or self.name_ka
