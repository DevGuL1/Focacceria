from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


def validate_max_video_size(value):
    if value and getattr(value, 'size', 0) > 40 * 1024 * 1024:
        raise ValidationError('Video file size must be 40MB or smaller.')


def validate_max_font_size(value):
    if value and getattr(value, 'size', 0) > 5 * 1024 * 1024:
        raise ValidationError('Font file size must be 5MB or smaller.')


video_file_validators = [
    FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'mov', 'm4v']),
    validate_max_video_size,
]


font_file_validators = [
    FileExtensionValidator(allowed_extensions=['woff', 'woff2', 'ttf', 'otf']),
    validate_max_font_size,
]


class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    logo_dark = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)

    tagline_ka = models.CharField(max_length=200, default='დაბადებული იტალიაში, გამომცხვარი თბილისში')
    tagline_en = models.CharField(max_length=200, default='Born in Italy, Baked in Tbilisi')

    phone = models.CharField(max_length=50, default='+995 598 80 00 45')
    address_ka = models.CharField(max_length=300, default='თბილისი, ძველი ქალაქი')
    address_en = models.CharField(max_length=300, default='Tbilisi, Old Town')

    opening_hours_ka = models.TextField(default='ორშ–პარ: 11:00–22:00\nშაბ–კვი: 10:00–23:00')
    opening_hours_en = models.TextField(default='Mon–Fri: 11:00–22:00\nSat–Sun: 10:00–23:00')

    instagram = models.URLField(blank=True, default='https://instagram.com/focacceria.ge')
    whatsapp = models.CharField(max_length=50, blank=True, default='+995598800045')
    email = models.EmailField(blank=True)
    google_maps_url = models.URLField(blank=True)
    wolt_url = models.URLField(blank=True)
    glovo_url = models.URLField(blank=True)
    delivery_wolt_icon = models.CharField(max_length=20, blank=True, default='🛵')
    delivery_glovo_icon = models.CharField(max_length=20, blank=True, default='🟡')
    delivery_call_icon = models.CharField(max_length=20, blank=True, default='📞')
    delivery_maps_icon = models.CharField(max_length=20, blank=True, default='📍')
    delivery_whatsapp_icon = models.CharField(max_length=20, blank=True, default='💬')
    menu_iframe_url = models.URLField(
        blank=True,
        default='https://focacceria.eat-me.online/en/category/mortadella'
    )
    menu_loader_enabled = models.BooleanField(default=True)

    about_title_ka = models.CharField(max_length=200, blank=True, default='ჩვენს შესახებ')
    about_title_en = models.CharField(max_length=200, blank=True, default='About Us')
    about_text_ka = models.TextField(blank=True)
    about_text_en = models.TextField(blank=True)
    about_image = models.ImageField(upload_to='site/', blank=True, null=True)

    show_about = models.BooleanField(default=True)
    show_visit = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_marquee = models.BooleanField(default=True)
    marquee_text_ka = models.CharField(
        max_length=500,
        default='SCHIACCIATA SANDWICHES · SALUMERIA CORNER · BORN IN ITALY · BAKED IN TBILISI'
    )
    marquee_text_en = models.CharField(
        max_length=500,
        default='SCHIACCIATA SANDWICHES · SALUMERIA CORNER · BORN IN ITALY · BAKED IN TBILISI'
    )

    story_kicker_ka = models.CharField(max_length=200, default='ჩვენი ისტორია', blank=True)
    story_kicker_en = models.CharField(max_length=200, default='Our Story', blank=True)
    story_title_ka = models.CharField(max_length=200, default='იტალია + თბილისი', blank=True)
    story_title_en = models.CharField(max_length=200, default='Italy + Tbilisi', blank=True)
    story_subtitle_ka = models.TextField(default='იტალიური ტექნიკა და ინგრედიენტები — თბილისის რიტმით.', blank=True)
    story_subtitle_en = models.TextField(default='Italian technique and ingredients — with Tbilisi rhythm.', blank=True)

    visit_kicker_ka = models.CharField(max_length=200, default='ვიზიტი', blank=True)
    visit_kicker_en = models.CharField(max_length=200, default='Visit', blank=True)
    visit_title_ka = models.CharField(max_length=200, default='მოდი, კარგად ჭამეთ', blank=True)
    visit_title_en = models.CharField(max_length=200, default='Come, eat well', blank=True)
    visit_subtitle_ka = models.TextField(default='დღეს ღიაა · ძველი ქალაქი, თბილისი', blank=True)
    visit_subtitle_en = models.TextField(default='Open today · Old Town, Tbilisi', blank=True)

    salumeria_kicker_ka = models.CharField(max_length=200, default='სალუმერია', blank=True)
    salumeria_kicker_en = models.CharField(max_length=200, default='Salumeria', blank=True)
    salumeria_title_ka = models.CharField(max_length=200, default='იტალიური დელიკატესები სახლში წასაღებად', blank=True)
    salumeria_title_en = models.CharField(max_length=200, default='Italian delicacies to take home', blank=True)
    salumeria_lead_ka = models.TextField(default='ხორცეული, ყველი, ზეთები და ნაკრები — შეკვეთა WhatsApp-ით.', blank=True)
    salumeria_lead_en = models.TextField(default='Cold cuts, cheese, oils and packages — order with WhatsApp.', blank=True)

    show_menu_products = models.BooleanField(default=True)

    whatsapp_widget_enabled = models.BooleanField(default=True)
    whatsapp_widget_phone = models.CharField(max_length=50, blank=True, default='')
    whatsapp_widget_message_ka = models.CharField(max_length=300, default='რითი დაგეხმაროთ?', blank=True)
    whatsapp_widget_message_en = models.CharField(max_length=300, default='How can we help you?', blank=True)

    class Meta:
        verbose_name = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class FontSettings(models.Model):
    heading_font_en_name = models.CharField(max_length=120, default='Anton')
    heading_font_en_url = models.URLField(
        blank=True,
        default='https://fonts.googleapis.com/css2?family=Anton&display=swap'
    )
    body_font_en_name = models.CharField(max_length=120, default='Inter')
    body_font_en_url = models.URLField(
        blank=True,
        default='https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
    )
    heading_font_ka_name = models.CharField(max_length=120, default='Noto Sans Georgian')
    heading_font_ka_file = models.FileField(
        upload_to='fonts/',
        blank=True,
        null=True,
        validators=font_file_validators,
    )
    body_font_ka_name = models.CharField(max_length=120, default='Noto Sans Georgian')
    body_font_ka_file = models.FileField(
        upload_to='fonts/',
        blank=True,
        null=True,
        validators=font_file_validators,
    )

    class Meta:
        verbose_name = 'Font Settings'

    def __str__(self):
        return 'Font Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HomeVideoSection(models.Model):
    EFFECT_CHOICES = [
        ('split', 'Split Reveal'),
        ('parallax', 'Parallax Reveal'),
    ]

    is_active = models.BooleanField(default=True)
    effect = models.CharField(max_length=20, choices=EFFECT_CHOICES, default='split')
    video_file = models.FileField(
        upload_to='home-video/',
        blank=True,
        null=True,
        validators=video_file_validators,
    )
    title_ka = models.CharField(max_length=220, blank=True, default='როგორ მზადდება გემო')
    title_en = models.CharField(max_length=220, blank=True, default='Where flavor gets made')
    subtitle_ka = models.TextField(
        blank=True,
        default='საფირმო შრეები, ტექსტურა და იტალიური ინგრედიენტები — ისე, თითქოს შენს თვალწინ მზადდება ყველაფერი.'
    )
    subtitle_en = models.TextField(
        blank=True,
        default='Signature layers, texture, and Italian ingredients — revealed as if the food is being prepared in front of you.'
    )

    class Meta:
        verbose_name = 'Home Video Section'

    def __str__(self):
        return 'Home Video Section'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HeroSlide(models.Model):
    image = models.ImageField(upload_to='slides/')
    product_image = models.ImageField(upload_to='slides/', blank=True, null=True)
    title_ka = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    subtitle_ka = models.CharField(max_length=400, blank=True)
    subtitle_en = models.CharField(max_length=400, blank=True)
    cta_text_ka = models.CharField(max_length=100, blank=True)
    cta_text_en = models.CharField(max_length=100, blank=True)
    cta_url = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title_en or self.title_ka or f'Slide {self.pk}'


class NavigationItem(models.Model):
    label_ka = models.CharField(max_length=100)
    label_en = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    open_new_tab = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label_en or self.label_ka


class FooterColumn(models.Model):
    title_ka = models.CharField(max_length=100, blank=True)
    title_en = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title_en or self.title_ka or f'Column {self.pk}'


class FooterLink(models.Model):
    column = models.ForeignKey(FooterColumn, on_delete=models.CASCADE, related_name='links', null=True, blank=True)
    label_ka = models.CharField(max_length=100)
    label_en = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    open_new_tab = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label_en or self.label_ka


class SEOSettings(models.Model):
    PAGE_CHOICES = [
        ('home', 'Home Page'),
        ('menu', 'Menu Page'),
        ('salumeria', 'Salumeria Page'),
    ]
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    title_ka = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    description_ka = models.TextField(max_length=500, blank=True)
    description_en = models.TextField(max_length=500, blank=True)
    keywords = models.TextField(blank=True)
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True)

    class Meta:
        verbose_name = 'SEO Settings'
        verbose_name_plural = 'SEO Settings'

    def __str__(self):
        return f'SEO: {self.get_page_display()}'
