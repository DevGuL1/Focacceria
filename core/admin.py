from django import forms
from django.contrib import admin
from .models import SiteSettings, HeroSlide, NavigationItem, FooterColumn, FooterLink, SEOSettings


class SiteSettingsAdminForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'custom_css': forms.Textarea(attrs={'rows': 16, 'class': 'vLargeTextField', 'style': 'font-family: monospace;'}),
            'custom_js': forms.Textarea(attrs={'rows': 16, 'class': 'vLargeTextField', 'style': 'font-family: monospace;'}),
        }


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsAdminForm
    fieldsets = (
        ('Branding', {'fields': ('logo', 'logo_dark', 'favicon', 'tagline_ka', 'tagline_en')}),
        ('Contact', {'fields': ('phone', 'address_ka', 'address_en', 'email', 'instagram', 'whatsapp', 'google_maps_url')}),
        ('Hours', {'fields': ('opening_hours_ka', 'opening_hours_en')}),
        ('Delivery', {'fields': (
            'wolt_url', 'glovo_url', 'delivery_wolt_icon', 'delivery_glovo_icon',
            'delivery_call_icon', 'delivery_maps_icon', 'delivery_whatsapp_icon',
        )}),
        ('Menu', {'fields': ('menu_iframe_url', 'menu_loader_enabled')}),
        ('About', {'fields': ('about_title_ka', 'about_title_en', 'about_text_ka', 'about_text_en', 'about_image')}),
        ('Home · Quick Section (About copy above order cards)', {
            'fields': (
                'quick_kicker_ka', 'quick_kicker_en', 'quick_title_ka', 'quick_title_en',
                'quick_lead_ka', 'quick_lead_en', 'quick_cta_ka', 'quick_cta_en',
            ),
        }),
        ('Custom Design (CSS / JS)', {
            'fields': ('custom_css', 'custom_js'),
            'description': 'Add custom CSS/JS here to change the site design without editing code. CSS is injected before </head>, JS before </body>.',
        }),
    )


admin.site.register(HeroSlide)
admin.site.register(NavigationItem)
admin.site.register(FooterColumn)
admin.site.register(FooterLink)
admin.site.register(SEOSettings)
