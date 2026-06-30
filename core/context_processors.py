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

    opening_hours_text = settings.opening_hours_ka if lang == 'ka' else settings.opening_hours_en
    site_hours = []
    if opening_hours_text:
        for line in opening_hours_text.splitlines():
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                parts = line.split(':', 1)
                site_hours.append({
                    'day': parts[0].strip(),
                    'time': parts[1].strip()
                })
            else:
                site_hours.append({
                    'day': line,
                    'time': ''
                })

    return {
        'site': settings,
        'font_settings': font_settings,
        'font_stylesheet_urls': font_stylesheet_urls,
        'active_heading_family': active_heading_family,
        'active_body_family': active_body_family,
        'nav_items': nav_items,
        'footer_columns': footer_columns,
        'current_lang': lang,
        'site_hours': site_hours,
    }
