from django.contrib import admin
from .models import SiteSettings, HeroSlide, NavigationItem, FooterColumn, FooterLink, SEOSettings

admin.site.register(SiteSettings)
admin.site.register(HeroSlide)
admin.site.register(NavigationItem)
admin.site.register(FooterColumn)
admin.site.register(FooterLink)
admin.site.register(SEOSettings)
