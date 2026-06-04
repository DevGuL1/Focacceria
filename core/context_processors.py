from .models import FontSettings, SiteSettings, NavigationItem, FooterColumn, FooterLink


def site_context(request):
    settings = SiteSettings.get_settings()
    font_settings = FontSettings.get_settings()
    nav_items = NavigationItem.objects.filter(is_active=True)
    footer_columns = FooterColumn.objects.prefetch_related('links').all()
    lang = request.session.get('lang', 'ka')
    font_stylesheet_urls = []

    if lang == 'en':
        for url in [font_settings.heading_font_en_url, font_settings.body_font_en_url]:
            if url and url not in font_stylesheet_urls:
                font_stylesheet_urls.append(url)
    elif 'https://fonts.googleapis.com/css2?family=Noto+Sans+Georgian:wght@400;500;600;700&display=swap' not in font_stylesheet_urls:
        font_stylesheet_urls.append('https://fonts.googleapis.com/css2?family=Noto+Sans+Georgian:wght@400;500;600;700&display=swap')

    if lang == 'ka':
        active_heading_family = font_settings.heading_font_ka_name or 'Noto Sans Georgian'
        active_body_family = font_settings.body_font_ka_name or 'Noto Sans Georgian'
    else:
        active_heading_family = font_settings.heading_font_en_name or 'Anton'
        active_body_family = font_settings.body_font_en_name or 'Inter'

    return {
        'site': settings,
        'font_settings': font_settings,
        'font_stylesheet_urls': font_stylesheet_urls,
        'active_heading_family': active_heading_family,
        'active_body_family': active_body_family,
        'nav_items': nav_items,
        'footer_columns': footer_columns,
        'current_lang': lang,
    }
